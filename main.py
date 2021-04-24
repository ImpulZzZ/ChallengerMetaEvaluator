from model.getCompositions            import get_compositions
from model.groupCompositions          import group_compositions_by_traits, group_compositions_by_champions
from model.filterCompositionGroups    import filter_composition_groups, filter_composition_groups_by_placement
from model.dissolveCompositionGroups  import dissolve_composition_groups

from view import main_gui               as main_gui
from view import composition_group_view as composition_group_view

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap

# starts the main gui
def run_main_gui():

    def build_filters(checkboxes):

        # initialize filter dictionary with following shape
        filters={
            "traits"   : {},
            "champions" : {},
            "placements": ui.placementFilter.value() 
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
            filters["champions"].update({ui.championFilter1.text() : ui.championFilterSlider1.value()})
        if checkboxes["champion2"]:
            filters["champions"].update({ui.championFilter2.text() : ui.championFilterSlider2.value()})
        if checkboxes["champion3"]:
            filters["champions"].update({ui.championFilter3.text() : ui.championFilterSlider3.value()})
        if checkboxes["champion4"]:
            filters["champions"].update({ui.championFilter4.text() : ui.championFilterSlider4.value()})

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
                "trait1"    : ui.traitFilterCheckBox1.isChecked(),
                "trait2"    : ui.traitFilterCheckBox2.isChecked(),
                "trait3"    : ui.traitFilterCheckBox3.isChecked(),
                "trait4"    : ui.traitFilterCheckBox4.isChecked(),
                "champion1" : ui.championFilterCheckBox1.isChecked(),
                "champion2" : ui.championFilterCheckBox2.isChecked(),
                "champion3" : ui.championFilterCheckBox3.isChecked(),
                "champion4" : ui.championFilterCheckBox4.isChecked(),
                "item"      : ui.itemFilterCheckBox.isChecked(),
                "regions" : {
                    "euw"       : ui.euwCheckBox.isChecked(),
                    "kr"        : ui.krCheckBox.isChecked()
                    }
                }

    #############################################################################
    def show_traits():

        nonlocal composition_groups_shown_in_table
        nonlocal latest_placement_filter

        considered_regions = {}

        checkboxes = get_checkboxes()

        reset_tableview(headers=["Occurences", "Traits"])

        no_regions_selected = True
        for region in checkboxes["regions"]:
            if checkboxes["regions"][region]:
                if regional_composition_groups[region]["grouped_by"] != "traits":
                    compositions = dissolve_composition_groups(regional_composition_groups[region]["groups"])
                    regional_composition_groups[region]["groups"]        = group_compositions_by_traits(compositions)
                    regional_composition_groups[region]["grouped_by"]    = "traits"

                considered_regions.update({region : regional_composition_groups[region]["groups"]})
                no_regions_selected = False

        # do nothing if no region was selected to load
        if no_regions_selected:
            return

        filters = build_filters(checkboxes)

        # loop over every considered region
        counter = 0
        for region in considered_regions:
            
            # apply possible filters on dataset
            composition_groups_shown_in_table = filter_composition_groups(considered_regions[region], filters)

            # loop over compisitiongroups of each region
            for composition_group in composition_groups_shown_in_table:
                
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

        nonlocal regional_composition_groups
        nonlocal composition_groups_shown_in_table
        nonlocal latest_placement_filter
        considered_regions = {}

        # verify which checkboxes are pressed or not pressed
        checkboxes = get_checkboxes()

        if not checkboxes["regions"]["euw"] and not checkboxes["regions"]["kr"]:
            return

        reset_tableview(headers=["Occurences", "Champions"])

        no_regions_selected = True
        for region in checkboxes["regions"]:
            if checkboxes["regions"][region]:
                if regional_composition_groups[region]["grouped_by"] != "champions":
                    compositions = dissolve_composition_groups(regional_composition_groups[region]["groups"])
                    regional_composition_groups[region]["groups"]        = group_compositions_by_champions(compositions)
                    regional_composition_groups[region]["grouped_by"]    = "champions"

                considered_regions.update({region : regional_composition_groups[region]["groups"]})
                no_regions_selected = False

        # do nothing if no region was selected to load
        if no_regions_selected:
            return

        filters = build_filters(checkboxes)

        # loop over every considered region
        counter = 0
        for region in considered_regions:

            # apply possible filters on dataset
            composition_groups_shown_in_table = filter_composition_groups(considered_regions[region], filters)

            # loop over compisitiongroups of each region
            for composition_group in composition_groups_shown_in_table:
                
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
        print("Work in Progress")

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
        selected_composition_group = composition_groups_shown_in_table[ui.tableWidget.currentItem().row()]

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
                    label = QLabel()
                    pixmap = QPixmap(item).scaled(30, 30)
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
        nonlocal regional_composition_groups

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
        if checkboxes["euw"] and not regional_composition_groups["euw"]["loaded"]:
            europe = get_compositions(  region              = "europe",
                                        games_per_player    = int(ui.gamesPerPlayer.text()),
                                        players_per_region  = int(ui.playersPerRegion.text()),
                                        current_patch       = ui.currentPatchFilter.text(),
                                        ranked_league       = considered_league)     

            # sort composition group by traits
            euw_comps_unsorted = group_compositions_by_traits(europe)
            euw_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)

            # fill the composition_group dictionary
            regional_composition_groups["euw"]["groups"]        = sorted(euw_comps_unsorted, key=lambda x: x.counter, reverse=True)
            regional_composition_groups["euw"]["grouped_by"]    = "traits"
            regional_composition_groups["euw"]["loaded"]        = True

            # green checkbox to signalize loading is done
            ui.euwCheckBox.setStyleSheet("color: green;")

        # if kr is checked and not already loaded
        if checkboxes["kr"] and not regional_composition_groups["kr"]["loaded"]:
            korea = get_compositions(   region              = "korea",
                                        games_per_player    = int(ui.gamesPerPlayer.text()),
                                        players_per_region  = int(ui.playersPerRegion.text()),
                                        current_patch       = ui.currentPatchFilter.text(),
                                        ranked_league       = considered_league)
            
            # sort composition group on occurences
            kr_comps_unsorted = group_compositions_by_traits(korea)
            kr_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)

            # fill the composition_group dictionary
            regional_composition_groups["kr"]["groups"]         = sorted(kr_comps_unsorted, key=lambda x: x.counter, reverse=True)
            regional_composition_groups["euw"]["grouped_by"]    = "traits"
            regional_composition_groups["kr"]["loaded"]         = True

            # green checkbox to signalize loading is done
            ui.krCheckBox.setStyleSheet("color: green;")

    ##############################################################################

    # setup the gui
    app = QApplication([])
    main_window = QMainWindow()
    ui = main_gui.Ui_mainWindow()
    ui.setupUi(main_window)

    # setup global variables
    CURRENT_PATCH = "11.8"
    CURRENT_SET_TRAITS = [  "Cultist",
                            "Daredevil",
                            "Divine",
                            "Dragonsoul",
                            "Elderwood",
                            "Enlightened",
                            "Exile",
                            "Fabled",
                            "Fortune",
                            "Ninja",
                            "Spirit",
                            "Boss",
                            "Warlord",
                            "Adept",
                            "Assassin",
                            "Blacksmith",
                            "Brawler",
                            "Duelist",
                            "Emperor",
                            "Executioner",
                            "Keeper",
                            "Mage",
                            "Mystic",
                            "Sharpshooter",
                            "Slayer",
                            "Syphoner",
                            "Vanguard"]
    CURRENT_SET_CHAMPIONS = [   "Aatrox",
                                "Shyvana",
                                "Zilean"]
    CURRENT_SET_ITEMS = [   "Bloodthirster",
                            "Redemption",
                            "Zephyr"]
    regional_composition_groups = {
        "euw" : {
            "groups"    : [],
            "grouped_by": "none",
            "loaded"    : False
        },
        "kr" : {
            "groups"    : [],
            "grouped_by": "none",
            "loaded"    : False
        }
    }
    latest_placement_filter = ui.placementFilter.value()
    composition_groups_shown_in_table = []
    COLUMN_COUNT = 15

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