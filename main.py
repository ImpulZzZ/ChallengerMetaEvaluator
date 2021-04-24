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

    # current list of composition groups that is shown in tableview
    filtered_composition_groups = []

    euw_composition_groups = {
        "groups"    : [],
        "grouped_by": "none",
        "loaded"    : False
    }

    kr_composition_groups = {
        "groups"    : [],
        "grouped_by": "none",
        "loaded"    : False
    }

    CURRENT_PATCH = "11.8"

    # list of current traits possible to choose in filter dropdown menu
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

    # list of current champions possible to choose in filter dropdown menu
    CURRENT_SET_CHAMPIONS = [   "Aatrox",
                                "Shyvana",
                                "Zilean"]

    # list of current items possible to choose in filter dropdown menu
    CURRENT_SET_ITEMS = [   "Bloodthirster",
                            "Redemption",
                            "Zephyr"]

    #############################################################################
    def traits_button_pressed():

        nonlocal filtered_composition_groups
        nonlocal latest_placement_filter

        # reset table view
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.clearContents()
        considered_regions = {}

        # verify which checkboxes are pressed or not pressed
        checkboxes = {  "euw"       : ui.euwCheckBox.isChecked(),
                        "kr"        : ui.krCheckBox.isChecked(),
                        "trait1"    : ui.traitFilterCheckBox1.isChecked(),
                        "trait2"    : ui.traitFilterCheckBox2.isChecked(),
                        "trait3"    : ui.traitFilterCheckBox3.isChecked(),
                        "trait4"    : ui.traitFilterCheckBox4.isChecked(),
                        "champion1" : ui.championFilterCheckBox1.isChecked(),
                        "champion2" : ui.championFilterCheckBox2.isChecked(),
                        "champion3" : ui.championFilterCheckBox3.isChecked(),
                        "champion4" : ui.championFilterCheckBox4.isChecked(),
                        "item"      : ui.itemFilterCheckBox.isChecked()
                        }

        if not checkboxes["euw"] and not checkboxes["kr"]:
            return

        # show maximum of 10 traits per composition
        COLUMN_COUNT = 15
        ui.tableWidget.setColumnCount(COLUMN_COUNT)

        headers = ["Occurences", "Traits"]
        for i in range(2, COLUMN_COUNT):
            headers.append("")
            
        ui.tableWidget.setHorizontalHeaderLabels(headers)

        if checkboxes["euw"]:
            # if composition group is not already grouped by traits, do it
            if euw_composition_groups["grouped_by"] != "traits":
                # dissolve current composition group
                compositions = dissolve_composition_groups(euw_composition_groups["groups"])
                # and create a new one, grouped by traits
                euw_composition_groups["groups"]        = group_compositions_by_traits(compositions)
                euw_composition_groups["grouped_by"]    = "traits"

            considered_regions.update({"euw" : euw_composition_groups["groups"]})

        if checkboxes["kr"]:
            # if composition group is not already grouped by traits, do it
            if kr_composition_groups["grouped_by"] != "traits":
                # dissolve current composition group
                compositions = dissolve_composition_groups(kr_composition_groups["groups"])
                # and create a new one, grouped by traits
                kr_composition_groups["groups"]     = group_compositions_by_traits(compositions)
                kr_composition_groups["grouped_by"] = "traits"

            considered_regions.update({"kr" : kr_composition_groups["groups"]})

        # loop over every considered region
        counter = 0
        for region in considered_regions:

            # initialize filter dictionary with following shape
            filters={"traits"   : {},
                    "champions" : {},
                    "placements": ui.placementFilter.value() 
                    }
        
            # build up filter dictionary by iterating over filter elements
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

            # apply possible filters on dataset
            filtered_composition_groups = filter_composition_groups(considered_regions[region], filters)

            filtered_composition_groups_2 = filtered_composition_groups

            # filter for placements if filter slider was changed
            if latest_placement_filter != ui.placementFilter.value():
                latest_placement_filter = ui.placementFilter.value()
                filtered_composition_groups_2 = filter_composition_groups_by_placement(filtered_composition_groups, latest_placement_filter)


            # loop over compisitiongroups of each region
            for composition_group in filtered_composition_groups_2:
                
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
    def champions_button_pressed():

        nonlocal euw_composition_groups
        nonlocal kr_composition_groups
        nonlocal filtered_composition_groups
        nonlocal latest_placement_filter
        considered_regions = {}

        # verify which checkboxes are pressed or not pressed
        checkboxes = {  "euw"       : ui.euwCheckBox.isChecked(),
                        "kr"        : ui.krCheckBox.isChecked(),
                        "trait1"    : ui.traitFilterCheckBox1.isChecked(),
                        "trait2"    : ui.traitFilterCheckBox2.isChecked(),
                        "trait3"    : ui.traitFilterCheckBox3.isChecked(),
                        "trait4"    : ui.traitFilterCheckBox4.isChecked(),
                        "champion1" : ui.championFilterCheckBox1.isChecked(),
                        "champion2" : ui.championFilterCheckBox2.isChecked(),
                        "champion3" : ui.championFilterCheckBox3.isChecked(),
                        "champion4" : ui.championFilterCheckBox4.isChecked(),
                        "item"      : ui.itemFilterCheckBox.isChecked()
                        }

        if not checkboxes["euw"] and not checkboxes["kr"]:
            return

        # reset table view
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.clearContents()

        # show maximum of 15 champions per composition
        COLUMN_COUNT = 15
        ui.tableWidget.setColumnCount(COLUMN_COUNT)

        headers = ["Occurences", "Champions"]
        for i in range(2, COLUMN_COUNT):
            headers.append("")
            
        ui.tableWidget.setHorizontalHeaderLabels(headers)

        if checkboxes["euw"]:
            # if composition group is not already grouped by champions, do it
            if euw_composition_groups["grouped_by"] != "champions":
                # dissolve current composition group
                compositions = dissolve_composition_groups(euw_composition_groups["groups"])
                # and create a new one, grouped by champions
                euw_composition_groups["groups"]        = group_compositions_by_champions(compositions)
                euw_composition_groups["grouped_by"]    = "champions"

            considered_regions.update({"euw" : euw_composition_groups["groups"]})

        if checkboxes["kr"]:
            # if composition group is not already grouped by champions, do it
            if kr_composition_groups["grouped_by"] != "champions":
                # dissolve current composition group
                compositions = dissolve_composition_groups(kr_composition_groups["groups"])
                # and create a new one, grouped by champions
                kr_composition_groups["groups"]     = group_compositions_by_champions(compositions)
                kr_composition_groups["grouped_by"] = "champions"

            considered_regions.update({"kr" : kr_composition_groups["groups"]})

        # loop over every considered region
        counter = 0
        for region in considered_regions:

            # initialize filter dictionary with following shape
            filters={"traits"   : {},
                    "champions" : {},
                    "placements": ui.placementFilter.value()
                    }
        
            # build up filter dictionary by iterating over filter elements
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

            # apply possible filters on dataset
            filtered_composition_groups = filter_composition_groups(considered_regions[region], filters)

            filtered_composition_groups_2 = filtered_composition_groups

            # filter for placements if filter slider was changed
            if latest_placement_filter != ui.placementFilter.value():
                latest_placement_filter = ui.placementFilter.value()
                filtered_composition_groups_2 = filter_composition_groups_by_placement(filtered_composition_groups, latest_placement_filter)

            # loop over compisitiongroups of each region
            for composition_group in filtered_composition_groups_2:
                
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
    def items_button_pressed():
        print("Work in Progress")

    #############################################################################
    def item_double_clicked():

        # prevents infinite loop of function calls
        ui.tableWidget.itemDoubleClicked = False

        popup.setupUi(popup_window)

        # reset table view
        popup.tableWidget.setRowCount(0)
        popup.tableWidget.clearContents()
        popup.tableWidget.setColumnCount(15)

        # get selected composition group
        selected_composition_group = filtered_composition_groups[ui.tableWidget.currentItem().row()]

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
    def load_data_button_pressed():
        # to modify outer variables in inner function
        nonlocal euw_composition_groups
        nonlocal kr_composition_groups

        # verify which checkboxes are pressed or not pressed
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
        if checkboxes["euw"] and not euw_composition_groups["loaded"]:
            europe = get_compositions(  region              = "europe",
                                        games_per_player    = int(ui.gamesPerPlayer.text()),
                                        players_per_region  = int(ui.playersPerRegion.text()),
                                        current_patch       = ui.currentPatchFilter.text(),
                                        ranked_league       = considered_league)     

            # sort composition group by traits
            euw_comps_unsorted = group_compositions_by_traits(europe)
            euw_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)

            # fill the composition_group dictionary
            euw_composition_groups["groups"]        = sorted(euw_comps_unsorted, key=lambda x: x.counter, reverse=True)
            euw_composition_groups["grouped_by"]    = "traits"
            euw_composition_groups["loaded"]        = True

            # green checkbox to signalize loading is done
            ui.euwCheckBox.setStyleSheet("color: green;")

        # if kr is checked and not already loaded
        if checkboxes["kr"] and not kr_composition_groups["loaded"]:
            korea = get_compositions(   region              = "korea",
                                        games_per_player    = int(ui.gamesPerPlayer.text()),
                                        players_per_region  = int(ui.playersPerRegion.text()),
                                        current_patch       = ui.currentPatchFilter.text(),
                                        ranked_league       = considered_league)
            
            # sort composition group on occurences
            kr_comps_unsorted = group_compositions_by_traits(korea)
            kr_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)

            # fill the composition_group dictionary
            kr_composition_groups["groups"]         = sorted(kr_comps_unsorted, key=lambda x: x.counter, reverse=True)
            euw_composition_groups["grouped_by"]    = "traits"
            kr_composition_groups["loaded"]         = True

            # green checkbox to signalize loading is done
            ui.krCheckBox.setStyleSheet("color: green;")

    #############################################################################
    # shows details of a compositiongroup
    def run_composition_group_view_gui():
        popup.setupUi(popup_window)
        popup_window.show()

    ##############################################################################

    # setup the gui
    app = QApplication([])
    main_window = QMainWindow()
    ui = main_gui.Ui_mainWindow()
    ui.setupUi(main_window)

    latest_placement_filter = ui.placementFilter.value()

    # bind functions to the buttons
    ui.traitsButton.clicked.connect(traits_button_pressed)
    ui.championsButton.clicked.connect(champions_button_pressed)
    ui.itemsButton.clicked.connect(items_button_pressed)
    ui.loadDataButton.clicked.connect(load_data_button_pressed)
    ui.tableWidget.itemDoubleClicked.connect(item_double_clicked)

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