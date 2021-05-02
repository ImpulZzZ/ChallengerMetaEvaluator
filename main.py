from model.getCompositions          import get_compositions
from model.groupCompositions        import group_compositions_by_traits, group_compositions
from model.filterCompositionGroups  import filter_composition_groups, filter_composition_groups_by_placement

from view import main_gui               as main_gui
from view import composition_group_view as composition_group_view

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap

import json

def extract_names_from_json(json_file):
    result = []
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current_stats in data:
            result.append(current_stats["name"])

    return sorted(result)

def create_name_to_id_map(jsonfile):
    result = {}
    with open(json_file) as jsonfile:
        data = json.load(jsonfile)

        for current_stats in data:
            result.update(current_stats["name"] : current_stats["id"])

    return result


# starts the main gui
def run_main_gui():

    def build_filters(checkboxes):

        # initialize filter dictionary with following shape
        filters={
            "traits"        : {},
            "champions"     : {},
            "placements"    : ui.placementFilter.value() ,
            "traitTier"    : checkboxes["traitTier"],
            "championStar" : checkboxes["championStar"]
            }

        if checkboxes["trait1"]:
            filters["traits"].update({ui.traitFilter1.currentText() : ui.traitFilterSlider1.value()})
        if checkboxes["trait2"]:
            filters["traits"].update({ui.traitFilter2.currentText() : ui.traitFilterSlider2.value()})
        if checkboxes["trait3"]:
            filters["traits"].update({ui.traitFilter3.currentText() : ui.traitFilterSlider3.value()})
        if checkboxes["trait4"]:
            filters["traits"].update({ui.traitFilter4.currentText() : ui.traitFilterSlider4.value()})
        if checkboxes["champion1"]:
            filters["champions"].update({ui.championFilter1.currentText() : ui.championFilterSlider1.value()})
        if checkboxes["champion2"]:
            filters["champions"].update({ui.championFilter2.currentText() : ui.championFilterSlider2.value()})
        if checkboxes["champion3"]:
            filters["champions"].update({ui.championFilter3.currentText() : ui.championFilterSlider3.value()})
        if checkboxes["champion4"]:
            filters["champions"].update({ui.championFilter4.currentText() : ui.championFilterSlider4.value()})

        return filters

    def reset_tableview(headers):  
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.clearContents()

        ui.tableWidget.setColumnCount(COLUMN_COUNT)

        for i in range(len(headers), COLUMN_COUNT):
            headers.append("")
            
        ui.tableWidget.setHorizontalHeaderLabels(headers)


    # verify which checkboxes are pressed or not pressed
    def get_checkboxes():
        
        return {
                "trait1"        : ui.traitFilterCheckBox1.isChecked(),
                "trait2"        : ui.traitFilterCheckBox2.isChecked(),
                "trait3"        : ui.traitFilterCheckBox3.isChecked(),
                "trait4"        : ui.traitFilterCheckBox4.isChecked(),
                "traitTier"     : ui.traitFilterTierCheckBox.isChecked(),
                "champion1"     : ui.championFilterCheckBox1.isChecked(),
                "champion2"     : ui.championFilterCheckBox2.isChecked(),
                "champion3"     : ui.championFilterCheckBox3.isChecked(),
                "champion4"     : ui.championFilterCheckBox4.isChecked(),
                "championStar"  : ui.championStarFilterCheckBox.isChecked(),
                "item"          : ui.itemFilterCheckBox.isChecked(),
                "regions" : {
                    "euw"   : ui.euwCheckBox.isChecked(),
                    "kr"    : ui.krCheckBox.isChecked()
                    }
                }

    #############################################################################
    def show_traits():

        nonlocal composition_group_database

        # verify which checkboxes are pressed or not pressed
        checkboxes = get_checkboxes()

        reset_tableview(headers=["Occurences", "Traits"])

        # validate which regions are selected and group them
        (considered_regions, composition_group_database) = group_compositions(  checkboxes          = checkboxes, 
                                                                                composition_groups  = composition_group_database, 
                                                                                group_by            = "traits")

        # validate which filters have to be applied
        filters = build_filters(checkboxes)

        # loop over every considered region
        counter = 0
        for region in considered_regions:

            # always filter for given placements
            composition_group_database["shown_in_table"] = filter_composition_groups_by_placement(  composition_groups  = considered_regions[region],
                                                                                                    max_placement       = filters["placements"])
            
            # apply other possible filters on dataset
            composition_group_database["shown_in_table"] = filter_composition_groups(   composition_groups  = composition_group_database["shown_in_table"], 
                                                                                        filters             = filters)

            # loop over compisitiongroups of each region
            for composition_group in composition_group_database["shown_in_table"]:
                
                # assert composition groups to be grouped by traits, so entries should be equal
                #   => consider only first entry
                element = composition_group.compositions[0]

                # change table size dynamically
                ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)

                # add the counter to table
                current_counter = QTableWidgetItem(str(composition_group.counter))
                ui.tableWidget.setItem(counter, 0, current_counter)

                # fill row starting at second index (counter is at first index)
                keycounter = 1

                for key in element.traits:
                    # add the elements into the table
                    current = QTableWidgetItem(str(key))
                    ui.tableWidget.setItem(counter, keycounter, current)

                    # background color depending on trait class
                    if element.traits[key] == 1:
                        ui.tableWidget.item(counter, keycounter).setBackground(QColor("brown"))
                    elif element.traits[key] == 2:
                        ui.tableWidget.item(counter, keycounter).setBackground(QColor("silver"))
                    elif element.traits[key] == 3:
                        ui.tableWidget.item(counter, keycounter).setBackground(QColor("gold"))
                    else:
                        ui.tableWidget.item(counter, keycounter).setBackground(QColor("cyan"))

                    keycounter = keycounter + 1

                counter = counter + 1

    #############################################################################
    def show_champions():

        nonlocal composition_group_database

        # verify which checkboxes are pressed or not pressed
        checkboxes = get_checkboxes()

        if not checkboxes["regions"]["euw"] and not checkboxes["regions"]["kr"]:
            return

        reset_tableview(headers=["Occurences", "Champions"])

        # validate which regions are selected and group them
        (considered_regions, composition_group_database) = group_compositions(  checkboxes          = checkboxes, 
                                                                                composition_groups  = composition_group_database, 
                                                                                group_by            = "champions")

        # validate which filters have to be applied
        filters = build_filters(checkboxes)

        # loop over every considered region
        counter = 0
        for region in considered_regions:

            # always filter for given placements
            composition_group_database["shown_in_table"] = filter_composition_groups_by_placement(  composition_groups  = considered_regions[region],
                                                                                                    max_placement       = filters["placements"])

            # apply other possible filters on dataset
            composition_group_database["shown_in_table"] = filter_composition_groups(   composition_groups  = composition_group_database["shown_in_table"], 
                                                                                        filters             = filters)

            # loop over compisitiongroups of each region
            for composition_group in composition_group_database["shown_in_table"]:
                
                # assert composition groups to be grouped by champions, so entries should be equal
                #   => only consider first entry
                element = composition_group.compositions[0]

                # change table size dynamically
                ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)

                # add the counter to table
                current_counter = QTableWidgetItem(str(composition_group.counter))
                ui.tableWidget.setItem(counter, 0, current_counter)

                # fill row starting at second index (counter is at first index)
                keycounter = 1

                for champion in element.champions:

                    current_champion = QTableWidgetItem()
                    label = QLabel()
                    pixmap = QPixmap(champion.icon).scaled(30, 30)
                    label.setPixmap(pixmap)
                    ui.tableWidget.setCellWidget(counter, keycounter, label)

                    # show amount of stars right to champion icon
                    if champion.tier == 1:
                        current_champion.setText("   *")
                    elif champion.tier == 2:
                        current_champion.setText("   **")
                    elif champion.tier == 3:
                        current_champion.setText("   ***")
                    else:
                        current_champion.setText("   ****")

                    current_champion.setFont(QFont('Arial', 24))
                    ui.tableWidget.setItem(counter, keycounter, current_champion)

                    keycounter = keycounter + 1

                counter = counter + 1

    #############################################################################
    def show_items():
        nonlocal composition_group_database

        # verify which checkboxes are pressed or not pressed
        checkboxes = get_checkboxes()

        if not checkboxes["regions"]["euw"] and not checkboxes["regions"]["kr"]:
            return

        reset_tableview(headers=["Occurences", "Champions"])

        # validate which regions are selected and group them
        (considered_regions, composition_group_database) = group_compositions(  checkboxes          = checkboxes, 
                                                                                composition_groups  = composition_group_database, 
                                                                                group_by            = "items")

        # validate which filters have to be applied
        filters = build_filters(checkboxes)

        # loop over every considered region
        row_counter = 0
        for region in considered_regions:

            # always filter for given placements
            composition_group_database["shown_in_table"] = filter_composition_groups_by_placement(  composition_groups  = considered_regions[region],
                                                                                                    max_placement       = filters["placements"])

            # apply other possible filters on dataset
            composition_group_database["shown_in_table"] = filter_composition_groups(   composition_groups  = composition_group_database["shown_in_table"], 
                                                                                        filters             = filters)

            # loop over compisitiongroups of each region
            for composition_group in composition_group_database["shown_in_table"]:
                
                # assert composition groups to be grouped by champions, so entries should be equal
                #   => only consider first entry
                element = composition_group.compositions[0]

                # change table size dynamically
                ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)

                # add the counter to table
                current_counter = QTableWidgetItem(str(composition_group.counter))
                ui.tableWidget.setItem(row_counter, 0, current_counter)

                for champion in element.champions:
                    if len(champion.items) > 0:
                        label = QLabel()
                        pixmap = QPixmap(champion.icon).scaled(30, 30)
                        label.setPixmap(pixmap)
                        ui.tableWidget.setCellWidget(row_counter, 1, label)

                        # add icons of the items on the side of champion
                        item_position = 2
                        for item in champion.item_icons:
                            label = QLabel()
                            pixmap = QPixmap(item).scaled(30, 30)
                            label.setPixmap(pixmap)
                            ui.tableWidget.setCellWidget(row_counter, item_position, label)
                            item_position += 1

                        # change table size dynamically
                        ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)
                        row_counter = row_counter + 1

                row_counter = row_counter + 1
        
        

    #############################################################################
    def show_composition_group():

        # prevents infinite loop of function calls
        ui.tableWidget.itemDoubleClicked = False

        popup.setupUi(popup_window)

        # reset table view
        popup.tableWidget.setRowCount(0)
        popup.tableWidget.clearContents()
        popup.tableWidget.setColumnCount(COLUMN_COUNT)

        # get selected composition group
        selected_composition_group = composition_group_database["shown_in_table"][ui.tableWidget.currentItem().row()]

        row_counter = 0
        for composition in selected_composition_group.compositions:

            # make space for placement row
            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)

            # show placement of compositon
            popup.tableWidget.setItem(row_counter, 0, QTableWidgetItem("Placement: " + str(composition.placement)))

            # make space for trait row
            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
            row_counter = row_counter + 1

            # show traits
            column_counter = 0
            for trait in composition.traits:
            
                current_trait = QTableWidgetItem(trait)
                popup.tableWidget.setItem(row_counter, column_counter, current_trait)

                # background color depending on trait class
                if composition.traits[trait] == 1:
                    popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("brown"))
                elif composition.traits[trait] == 2:
                    popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("silver"))
                elif composition.traits[trait] == 3:
                    popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("gold"))
                else:
                    popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("cyan"))

                column_counter = column_counter + 1

            # make space for first champion
            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
            row_counter = row_counter + 1

            # show each champion
            for champion in composition.champions:
            
                current_champion = QTableWidgetItem()

                label = QLabel()
                pixmap = QPixmap(champion.icon).scaled(30, 30)
                label.setPixmap(pixmap)
                popup.tableWidget.setCellWidget(row_counter, 0, label)

                # show amount of stars right to champion icon
                if champion.tier == 1:
                    current_champion.setText("   *")
                elif champion.tier == 2:
                    current_champion.setText("   **")
                elif champion.tier == 3:
                    current_champion.setText("   ***")
                else:
                    current_champion.setText("   ****")

                current_champion.setFont(QFont('Arial', 24))
                popup.tableWidget.setItem(row_counter, 0, current_champion)

                # add icons of the items on the side of champion
                item_position = 1
                for item in champion.item_icons:
                    label   = QLabel()
                    pixmap  = QPixmap(item).scaled(30, 30)
                    label.setPixmap(pixmap)
                    popup.tableWidget.setCellWidget(row_counter, item_position, label)
                    item_position += 1

                # make space for next champion
                popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
                row_counter = row_counter + 1

            # create an empty row to divide compositions
            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
            row_counter = row_counter + 1
        
        popup_window.show()
        
    #############################################################################
    def load_data():
        # to modify outer variables in inner function
        nonlocal composition_group_database

        # verify which loading checkboxes are pressed or not pressed
        checkboxes = {  "euw"           : ui.euwCheckBox.isChecked(),
                        "kr"            : ui.krCheckBox.isChecked(),
                        "challenger"    : ui.challengerCheckBox.isChecked(),
                        "grandmaster"   : ui.grandmasterCheckBox.isChecked(),
                        "master"        : ui.masterCheckBox.isChecked()}

        # if no regions are chosen, do nothing
        if not checkboxes["euw"] and not checkboxes["kr"]:
            return

        # choose highest league of checked ones
        if checkboxes["challenger"]:
            considered_league = "master"
        else:
            if checkboxes["grandmaster"]:
                considered_league = "grandmaster"
            else:
                if checkboxes["master"]:
                    considered_league = "master"
                else:
                    # do nothing if no league checked
                    return

        # if euw is checked and not already loaded
        if checkboxes["euw"] and not composition_group_database["euw"]["loaded"]:
            europe = get_compositions(  region              = "europe",
                                        games_per_player    = int(ui.gamesPerPlayer.text()),
                                        players_per_region  = int(ui.playersPerRegion.text()),
                                        current_patch       = ui.currentPatchFilter.text(),
                                        ranked_league       = considered_league)     

            # sort composition group by traits
            euw_comps_unsorted = group_compositions_by_traits(europe)
            euw_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)

            # fill the composition_group dictionary
            composition_group_database["euw"]["database"]   = sorted(euw_comps_unsorted, key=lambda x: x.counter, reverse=True)
            composition_group_database["euw"]["grouped_by"] = "traits"
            composition_group_database["euw"]["loaded"]     = True

            # green checkbox to signalize loading is done
            ui.euwCheckBox.setStyleSheet("color: green;")

        # if kr is checked and not already loaded
        if checkboxes["kr"] and not composition_group_database["kr"]["loaded"]:
            korea = get_compositions(   region              = "korea",
                                        games_per_player    = int(ui.gamesPerPlayer.text()),
                                        players_per_region  = int(ui.playersPerRegion.text()),
                                        current_patch       = ui.currentPatchFilter.text(),
                                        ranked_league       = considered_league)
            
            # sort composition group on occurences
            kr_comps_unsorted = group_compositions_by_traits(korea)
            kr_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)

            # fill the composition_group dictionary
            composition_group_database["kr"]["database"]    = sorted(kr_comps_unsorted, key=lambda x: x.counter, reverse=True)
            composition_group_database["euw"]["grouped_by"] = "traits"
            composition_group_database["kr"]["loaded"]      = True

            # green checkbox to signalize loading is done
            ui.krCheckBox.setStyleSheet("color: green;")

    ##############################################################################

    # setup the gui
    app         = QApplication([])
    main_window = QMainWindow()
    ui          = main_gui.Ui_mainWindow()
    ui.setupUi(main_window)

    # setup global variables
    COLUMN_COUNT                = 15
    CURRENT_PATCH               = "11.9"
    STATIC_DATA_DIR             = "Set5_static_data/"
    CURRENT_SET_TRAITS          = extract_names_from_json(STATIC_DATA_DIR + "traits.json")
    CURRENT_SET_CHAMPIONS       = extract_names_from_json(STATIC_DATA_DIR + "champions.json")
    CURRENT_SET_ITEMS           = extract_names_from_json(STATIC_DATA_DIR + "items.json")
    ITEM_NAME_TO_ID_MAP         = create_name_to_id_map(STATIC_DATA_DIR + "items.json")
    composition_group_database  = {
        "euw" : {
            "database"      : [],
            "grouped_by"    : "none",
            "loaded"        : False
        },
        "kr" : {
            "database"      : [],
            "grouped_by"    : "none",
            "loaded"        : False
        },
        "shown_in_table"    : []  
    }

    # bind functions to the buttons
    ui.traitsButton.clicked.connect(show_traits)
    ui.championsButton.clicked.connect(show_champions)
    ui.itemsButton.clicked.connect(show_items)
    ui.tableWidget.itemDoubleClicked.connect(show_composition_group)
    ui.loadDataButton.clicked.connect(load_data)

    # add traits to dropdown filters
    ui.traitFilter1.addItems(CURRENT_SET_TRAITS)
    ui.traitFilter2.addItems(CURRENT_SET_TRAITS)
    ui.traitFilter3.addItems(CURRENT_SET_TRAITS)
    ui.traitFilter4.addItems(CURRENT_SET_TRAITS)
    ui.championFilter1.addItems(CURRENT_SET_CHAMPIONS)
    ui.championFilter2.addItems(CURRENT_SET_CHAMPIONS)
    ui.championFilter3.addItems(CURRENT_SET_CHAMPIONS)
    ui.championFilter4.addItems(CURRENT_SET_CHAMPIONS)
    ui.itemFilter.addItems(CURRENT_SET_ITEMS)

    # current patch
    ui.currentPatchFilter.setText(CURRENT_PATCH)

    # setup the other guis
    popup_window = QMainWindow()
    popup = composition_group_view.Ui_compositionGroupView()

    main_window.show()
    app.exec_()


run_main_gui()