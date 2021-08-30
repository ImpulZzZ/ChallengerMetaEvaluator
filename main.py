from view import main_gui               as main_gui
from view import composition_group_view as composition_group_view
from PyQt5.QtWidgets                import *
from PyQt5.QtGui                    import QColor, QFont, QPixmap
from model.CompositionGroup         import CompositionGroup
from model.Data                     import Data
from model.sortUtilities            import sort_composition_groups_by_occurence_and_placement
from model.bestInSlot               import compute_best_in_slot
from model.getCompositions          import get_compositions, request_api
from model.groupCompositions        import group_compositions_by_traits, group_compositions
from model.groupCompositionGroups   import group_composition_groups_by_n_traits
from model.filterCompositionGroups  import filter_composition_groups, filter_composition_groups_by_placement
from model.bestInSlot               import compute_best_in_slot

import requests

def run_main_gui():

    def build_filters(checkboxes):
        filters={
            "traits"       : {},
            "champions"    : {},
            "items"        : [],
            "placements"   : ui.placementFilter.value(),
            "traitTier"    : checkboxes["traitTier"],
            "championStar" : checkboxes["championStar"]
            }

        if checkboxes["item1"]: filters["items"].append(ui.itemFilter1.currentText())
        if checkboxes["item2"]: filters["items"].append(ui.itemFilter2.currentText())
        if checkboxes["item3"]: filters["items"].append(ui.itemFilter3.currentText())
        if checkboxes["item4"]: filters["items"].append(ui.itemFilter4.currentText())

        if checkboxes["trait1"]: filters["traits"].update({ui.traitFilter1.currentText() : ui.traitFilterSlider1.value()})
        if checkboxes["trait2"]: filters["traits"].update({ui.traitFilter2.currentText() : ui.traitFilterSlider2.value()})
        if checkboxes["trait3"]: filters["traits"].update({ui.traitFilter3.currentText() : ui.traitFilterSlider3.value()})
        if checkboxes["trait4"]: filters["traits"].update({ui.traitFilter4.currentText() : ui.traitFilterSlider4.value()})

        if checkboxes["champion1"]: filters["champions"].update({ui.championFilter1.currentText() : ui.championFilterSlider1.value()})
        if checkboxes["champion2"]: filters["champions"].update({ui.championFilter2.currentText() : ui.championFilterSlider2.value()})
        if checkboxes["champion3"]: filters["champions"].update({ui.championFilter3.currentText() : ui.championFilterSlider3.value()})
        if checkboxes["champion4"]: filters["champions"].update({ui.championFilter4.currentText() : ui.championFilterSlider4.value()})

        return filters

    def reset_tableview(headers):  
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.clearContents()
        ui.tableWidget.setColumnCount(COLUMN_COUNT)

        for i in range(len(headers), COLUMN_COUNT): 
            headers.append("")
            
        ui.tableWidget.setHorizontalHeaderLabels(headers)

    def get_checkboxes():
        
        return {
                "trait1"              : ui.traitFilterCheckBox1.isChecked(),
                "trait2"              : ui.traitFilterCheckBox2.isChecked(),
                "trait3"              : ui.traitFilterCheckBox3.isChecked(),
                "trait4"              : ui.traitFilterCheckBox4.isChecked(),
                "traitTier"           : ui.traitFilterTierCheckBox.isChecked(),
                "ignoreOneUnitTraits" : ui.one_unit_trait_ignore_checkbox.isChecked(),
                "champion1"           : ui.championFilterCheckBox1.isChecked(),
                "champion2"           : ui.championFilterCheckBox2.isChecked(),
                "champion3"           : ui.championFilterCheckBox3.isChecked(),
                "champion4"           : ui.championFilterCheckBox4.isChecked(),
                "championStar"        : ui.championStarFilterCheckBox.isChecked(),
                "item1"               : ui.itemFilterCheckBox1.isChecked(),
                "item2"               : ui.itemFilterCheckBox2.isChecked(),
                "item3"               : ui.itemFilterCheckBox3.isChecked(),
                "item4"               : ui.itemFilterCheckBox4.isChecked(),
                "regions" : {
                    "euw" : ui.euwCheckBox.isChecked(),
                    "kr"  : ui.krCheckBox.isChecked()
                    }
                }

    def initialize_variables(group_by):
        nonlocal composition_group_database

        checkboxes = get_checkboxes()
        filters    = build_filters(checkboxes)
        reset_tableview(["Occurences", "Avg Placement", "Traits"])
        (considered_regions, composition_group_database) = group_compositions(checkboxes, composition_group_database, group_by)

        return (considered_regions, filters)
    
    def show_traits():
        nonlocal composition_group_database

        (considered_regions, filters) = initialize_variables(group_by = "traits")
        counter = 0
        for region in considered_regions:

            composition_group_database["shown_in_table"] = filter_composition_groups_by_placement(composition_groups = considered_regions[region],
                                                                                                  max_placement      = filters["placements"])

            composition_group_database["shown_in_table"] = filter_composition_groups(composition_groups = composition_group_database["shown_in_table"], 
                                                                                     filters            = filters)
            
            for composition_group in composition_group_database["shown_in_table"]:
                if composition_group.counter < int(ui.minOccurencesFilter.text()): continue
                
                ## Assert composition groups to be grouped by traits, so entry 0 equals entry n
                element = composition_group.compositions[0]

                ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)

                ## Add counter to table
                current_counter = QTableWidgetItem(str(composition_group.counter))
                ui.tableWidget.setItem(counter, 0, current_counter)

                ## Add average placement to table
                current_avg_placement = QTableWidgetItem(str(composition_group.avg_placement))
                ui.tableWidget.setItem(counter, 1, current_avg_placement)

                ## Fill row starting at second index
                keycounter = 2
                for key in element.traits:
                    ## Add the elements into the table
                    current = QTableWidgetItem(str(key))
                    ui.tableWidget.setItem(counter, keycounter, current)

                    ## Background color depending on trait class
                    if   element.traits[key] == 1: ui.tableWidget.item(counter, keycounter).setBackground(QColor("brown"))
                    elif element.traits[key] == 2: ui.tableWidget.item(counter, keycounter).setBackground(QColor("silver"))
                    elif element.traits[key] == 3: ui.tableWidget.item(counter, keycounter).setBackground(QColor("gold"))
                    else:                          ui.tableWidget.item(counter, keycounter).setBackground(QColor("cyan"))

                    keycounter += 1
                counter += 1

    def show_n_traits():
        nonlocal composition_group_database

        (considered_regions, filters) = initialize_variables(group_by = "traits")
        counter = 0
        for region in considered_regions:

            composition_group_database["shown_in_table"] = filter_composition_groups_by_placement(composition_groups = considered_regions[region],
                                                                                                  max_placement      = filters["placements"])

            composition_group_database["shown_in_table"] = filter_composition_groups(composition_groups = composition_group_database["shown_in_table"], 
                                                                                     filters            = filters)
            
            combination_dict = group_composition_groups_by_n_traits(composition_groups     = composition_group_database["shown_in_table"],
                                                                    n                      = ui.nTraitFilterSlider.value(),
                                                                    ignore_one_unit_traits = ui.one_unit_trait_ignore_checkbox.isChecked())
            composition_groups = []
            for combination in combination_dict:
                composition_groups.append(CompositionGroup(combination_dict[combination]["compositions"]))

            composition_group_database["shown_in_table"]     = composition_groups
            composition_group_database[region]["grouped_by"] = "n_traits"

            for combination in combination_dict:
                if combination_dict[combination]["counter"] < int(ui.minOccurencesFilter.text()): continue
                
                trait_combinations = combination.split('+')
                
                ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)

                current_counter = QTableWidgetItem(str(combination_dict[combination]["counter"]))
                ui.tableWidget.setItem(counter, 0, current_counter)

                current_avg_placement = QTableWidgetItem(str(combination_dict[combination]["avg_placement"]))
                ui.tableWidget.setItem(counter, 1, current_avg_placement)

                ## Fill row starting at second index
                keycounter = 2
                for trait_combination in trait_combinations:
                    (tier, trait) = trait_combination.split('--')
                    tier = int(tier)

                    current = QTableWidgetItem(trait)
                    ui.tableWidget.setItem(counter, keycounter, current)

                    ## Background color depending on trait class
                    if   tier == 1:   ui.tableWidget.item(counter, keycounter).setBackground(QColor("brown"))
                    elif tier == 2:   ui.tableWidget.item(counter, keycounter).setBackground(QColor("silver"))
                    elif tier == 3:   ui.tableWidget.item(counter, keycounter).setBackground(QColor("gold"))
                    else:             ui.tableWidget.item(counter, keycounter).setBackground(QColor("cyan"))

                    keycounter += 1
                counter += 1

    def show_champions():
        nonlocal composition_group_database

        (considered_regions, filters) = initialize_variables(group_by = "champions")

        # TODO: at the moment regions are just grouped within theirselves and not with other regions
        counter = 0
        for region in considered_regions:

            composition_group_database["shown_in_table"] = filter_composition_groups_by_placement(composition_groups = considered_regions[region],
                                                                                                  max_placement      = filters["placements"])

            composition_group_database["shown_in_table"] = filter_composition_groups(composition_groups = composition_group_database["shown_in_table"], 
                                                                                     filters            = filters)
            for composition_group in composition_group_database["shown_in_table"]:
                if composition_group.counter < int(ui.minOccurencesFilter.text()): continue
                
                element = composition_group.compositions[0]

                ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)

                ## Add counter to table
                current_counter = QTableWidgetItem(str(composition_group.counter))
                ui.tableWidget.setItem(counter, 0, current_counter)

                ## Add average placement to table
                current_avg_placement = QTableWidgetItem(str(composition_group.avg_placement))
                ui.tableWidget.setItem(counter, 1, current_avg_placement)

                keycounter = 2
                for champion in element.champions:

                    current_champion = QTableWidgetItem()
                    label            = QLabel()
                    pixmap           = QPixmap(champion.icon).scaled(30, 30)
                    label.setPixmap(pixmap)
                    ui.tableWidget.setCellWidget(counter, keycounter, label)

                    current_champion.setFont(QFont('Arial', 24))
                    ui.tableWidget.setItem(counter, keycounter, current_champion)

                    keycounter += 1
                counter += 1
    
    def show_best_in_slot():
        nonlocal composition_group_database
        composition_groups = []
        item_amount        = ui.bestInSlotSlider.value()

        reset_tableview(headers=["Champion", "Items", "", "", "Occurences", "Avg Placement"])

        checkboxes = get_checkboxes()
        filters    = build_filters(checkboxes)
        champions  = filters["champions"]

        if len(champions) == 0: champions = data.champions

        ## Merge all data from regions together
        for region in composition_group_database:
            try: composition_groups.append(composition_group_database[region]["database"])
            except TypeError: continue

        bis_dict = compute_best_in_slot(composition_groups, item_amount)

        ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)
        
        row_counter = 0
        for champion in champions:
            label  = QLabel()
            pixmap = QPixmap(f"{data.data_dir}/champions/TFT5_{champion}.png").scaled(30, 30)
            label.setPixmap(pixmap)
            ui.tableWidget.setCellWidget(row_counter, 0, label)

            ## Exception handling, when bis was not found for a champion 
            try:
                if len(bis_dict[champion]) == 0:
                        error_text = QTableWidgetItem()
                        error_text.setText("NaN")
                        ui.tableWidget.setItem(row_counter, 1, error_text)

                for item_combination in bis_dict[champion]:
                    items = item_combination.split("+")

                    current_counter       = QTableWidgetItem()
                    current_avg_placement = QTableWidgetItem()
                    current_counter.setText(str(bis_dict[champion][item_combination]["counter"]))
                    current_avg_placement.setText(str(bis_dict[champion][item_combination]["avg_placement"]))

                    item_position = 1
                    for item in items:
                        label  = QLabel()
                        pixmap = QPixmap(f"{data.data_dir}/items/{item}.png").scaled(30, 30)
                        label.setPixmap(pixmap)
                        ui.tableWidget.setCellWidget(row_counter, item_position, label)
                        item_position += 1

                    ui.tableWidget.setItem(row_counter, 4, current_counter)
                    ui.tableWidget.setItem(row_counter, 5, current_avg_placement)

                    ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)
                    row_counter += 1
            
            except KeyError:
                error_text = QTableWidgetItem()
                error_text.setText("NaN")
                ui.tableWidget.setItem(row_counter, 1, error_text)

            ui.tableWidget.setRowCount(ui.tableWidget.rowCount() + 1)
            row_counter += 1

    def show_composition_group():
        ## Prevents infinite loop of function calls
        ui.tableWidget.itemDoubleClicked = False

        ## TODO show_composition_group doesnt work properly for other cases 
        if composition_group_database["euw"]["grouped_by"] not in ["traits", "champions", "n_traits"]: return

        popup.setupUi(popup_window)
        popup.tableWidget.setRowCount(0)
        popup.tableWidget.clearContents()
        popup.tableWidget.setColumnCount(COLUMN_COUNT)

        ## Get selected composition group
        selected_composition_group = composition_group_database["shown_in_table"][ui.tableWidget.currentItem().row()]

        row_counter = 0
        for composition in selected_composition_group.compositions:
            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)

            popup.tableWidget.setItem(row_counter, 0, QTableWidgetItem(f"Placement: {str(composition.placement)}"))

            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
            row_counter += 1

            column_counter = 0
            for trait in composition.traits:
                current_trait = QTableWidgetItem(trait)
                popup.tableWidget.setItem(row_counter, column_counter, current_trait)

                ## Background color depending on trait class
                if   composition.traits[trait] == 1: popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("brown"))
                elif composition.traits[trait] == 2: popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("silver"))
                elif composition.traits[trait] == 3: popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("gold"))
                else:                                popup.tableWidget.item(row_counter, column_counter).setBackground(QColor("cyan"))

                column_counter += 1

            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
            row_counter += 1

            for champion in composition.champions:
            
                current_champion = QTableWidgetItem()
                label            = QLabel()
                pixmap           = QPixmap(champion.icon).scaled(30, 30)
                label.setPixmap(pixmap)
                popup.tableWidget.setCellWidget(row_counter, 0, label)

                ## Show amount of stars right to champion icon
                if   champion.tier == 1: current_champion.setText("   *")
                elif champion.tier == 2: current_champion.setText("   **")
                elif champion.tier == 3: current_champion.setText("   ***")
                else:                    current_champion.setText("   ****")

                current_champion.setFont(QFont('Arial', 24))
                popup.tableWidget.setItem(row_counter, 0, current_champion)

                item_position = 1
                for item in champion.items:
                    if item.not_component:
                        label  = QLabel()
                        pixmap = QPixmap(item.icon).scaled(30, 30)
                        label.setPixmap(pixmap)
                        popup.tableWidget.setCellWidget(row_counter, item_position, label)
                        item_position += 1

                popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
                row_counter += 1

            ## Create an empty row to divide compositions
            popup.tableWidget.setRowCount(popup.tableWidget.rowCount() + 1)
            row_counter += 1
        
        popup_window.show()

    def reset_data():
        nonlocal composition_group_database

        composition_group_database  = {
            "euw" : {
                "database"   : [],
                "grouped_by" : "none",
                "loaded"     : False
            },
            "kr" : {
                "database"   : [],
                "grouped_by" : "none",
                "loaded"     : False
            },
            "shown_in_table" : []}

        ui.euwCheckBox.setStyleSheet("color: black;")
        ui.krCheckBox.setStyleSheet("color: black;")
        ui.challengerCheckBox.setStyleSheet("color: black;")
        ui.grandmasterCheckBox.setStyleSheet("color: black;")
        ui.masterCheckBox.setStyleSheet("color: black;")
        ui.analyzedMatchesCounter.setText("0")
        ui.analyzedCompsCounter.setText("0")

    def load_data():
        nonlocal composition_group_database

        checkboxes = {"euw"         : ui.euwCheckBox.isChecked(),
                      "kr"          : ui.krCheckBox.isChecked(),
                      "challenger"  : ui.challengerCheckBox.isChecked(),
                      "grandmaster" : ui.grandmasterCheckBox.isChecked(),
                      "master"      : ui.masterCheckBox.isChecked()}

        if not checkboxes["euw"] and not checkboxes["kr"]: return

        ## Choose highest league of checked ones
        if checkboxes["challenger"]:
            considered_league = "challenger"
            ui.challengerCheckBox.setStyleSheet("color: green;")
        else:
            if checkboxes["grandmaster"]:
                considered_league = "grandmaster"
                ui.grandmasterCheckBox.setStyleSheet("color: green;")
            else:
                if checkboxes["master"]:
                    considered_league = "master"
                    ui.masterCheckBox.setStyleSheet("color: green;")
                else: return

        if checkboxes["euw"] and not composition_group_database["euw"]["loaded"]:
            europe = get_compositions(region             = "europe",
                                      games_per_player   = int(ui.gamesPerPlayer.text()),
                                      players_per_region = int(ui.playersPerRegion.text()),
                                      current_patch      = ui.currentPatchFilter.text(),
                                      ranked_league      = considered_league)

            euw_comps_unsorted = group_compositions_by_traits(europe["compositions"])

            composition_group_database["euw"]["database"]   = sort_composition_groups_by_occurence_and_placement(euw_comps_unsorted)
            composition_group_database["euw"]["grouped_by"] = "traits"
            composition_group_database["euw"]["loaded"]     = True

            ui.euwCheckBox.setStyleSheet("color: green;")
            ui.analyzedMatchesCounter.setText(str(europe["analyzed_games"]))
            ui.analyzedCompsCounter.setText(str(len(europe["compositions"])))

        if checkboxes["kr"] and not composition_group_database["kr"]["loaded"]:
            korea = get_compositions(region             = "korea",
                                     games_per_player   = int(ui.gamesPerPlayer.text()),
                                     players_per_region = int(ui.playersPerRegion.text()),
                                     current_patch      = ui.currentPatchFilter.text(),
                                     ranked_league      = considered_league)
            
            kr_comps_unsorted = group_compositions_by_traits(korea["compositions"])

            composition_group_database["kr"]["database"]    = sort_composition_groups_by_occurence_and_placement(kr_comps_unsorted)
            composition_group_database["euw"]["grouped_by"] = "traits"
            composition_group_database["kr"]["loaded"]      = True

            ui.krCheckBox.setStyleSheet("color: green;")
            ui.analyzedMatchesCounter.setText(str(korea["analyzed_games"]))
            ui.analyzedCompsCounter.setText(str(len(korea["compositions"])))

    ## Setup global variables
    data                       = Data()
    COLUMN_COUNT               = 15
    composition_group_database = {}
    
    ## Check api key and service
    api_key       = open("apikey.txt", "r").read()
    test_response = requests.get(f"https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/ImpulZzZ?api_key={api_key}")

    if test_response.status_code != 200: 
        print(test_response.content)
        return
    
    ## Setup the gui
    app         = QApplication([])
    main_window = QMainWindow()
    ui          = main_gui.Ui_mainWindow()
    ui.setupUi(main_window)
    reset_data()

    ## Bind functions to the buttons
    ui.traitsButton.clicked.connect(show_traits)
    ui.groupNTraitsButton.clicked.connect(show_n_traits)
    ui.championsButton.clicked.connect(show_champions)
    ui.tableWidget.itemDoubleClicked.connect(show_composition_group)
    ui.loadDataButton.clicked.connect(load_data)
    ui.resetDataButton.clicked.connect(reset_data)
    ui.bestInSlotButton.clicked.connect(show_best_in_slot)

    ## Add traits to dropdown filters
    ui.traitFilter1.addItems(data.traits)
    ui.traitFilter2.addItems(data.traits)
    ui.traitFilter3.addItems(data.traits)
    ui.traitFilter4.addItems(data.traits)
    ui.championFilter1.addItems(data.champions)
    ui.championFilter2.addItems(data.champions)
    ui.championFilter3.addItems(data.champions)
    ui.championFilter4.addItems(data.champions)
    ui.itemFilter1.addItems(data.items)
    ui.itemFilter2.addItems(data.items)
    ui.itemFilter3.addItems(data.items)
    ui.itemFilter4.addItems(data.items)

    ui.currentPatchFilter.setText(data.current_patch)

    ## Setup the other guis
    popup_window = QMainWindow()
    popup        = composition_group_view.Ui_compositionGroupView()

    main_window.show()
    app.exec_()

run_main_gui()