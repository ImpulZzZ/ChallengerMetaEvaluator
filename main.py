from model.functions.getCompositions          import get_compositions
from model.functions.groupCompositions        import group_compositions_by_traits
from model.functions.filterCompositionGroups  import filter_composition_groups

from view import main_gui               as main_gui
from view import composition_group_view as composition_group_view

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor

# starts the main gui
def run_main_gui():

    # initialize composition group fields
    euw_comps           = []
    kr_comps            = []

    # boolean whether or not region data was loaded from api
    euw_loaded          = False
    kr_loaded           = False

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

    #############################################################################
    def traits_button_pressed():

        # reset table view
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.clearContents()

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
                        "champion4" : ui.championFilterCheckBox4.isChecked()
                        }

        if not checkboxes["euw"] and not checkboxes["kr"]:
            return

        considered_regions = {}

        # show maximum of 10 traits per composition
        COLUMN_COUNT = 15
        ui.tableWidget.setColumnCount(COLUMN_COUNT)

        headers = ["Occurences", "Traits"]
        for i in range(2, COLUMN_COUNT):
            headers.append("")
            
        ui.tableWidget.setHorizontalHeaderLabels(headers)

        if checkboxes["euw"]:
            considered_regions.update({"euw" : euw_comps})

        if checkboxes["kr"]:
            considered_regions.update({"kr" : kr_comps})

        # loop over every considered region
        counter = 0
        for region in considered_regions:

            # initialize filter dictionary with following shape
            filters={"traits"   : {},
                    "champions" : {},
                    "placements": [] 
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

            # loop over compisitiongroups of each region
            for composition_group in filtered_composition_groups:
                
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
                    current = QTableWidgetItem(str(element.traits[key]) + " " + str(key))
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
    def compositions_button_pressed():
        print("Work in Progress")

    #############################################################################
    def champions_button_pressed():
        # reset table view
        ui.tableWidget.setRowCount(0)
        ui.tableWidget.clearContents()

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
                        "champion4" : ui.championFilterCheckBox4.isChecked()
                        }

        if not checkboxes["euw"] and not checkboxes["kr"]:
            return

        considered_regions = {}

        # show maximum of 15 champions per composition
        COLUMN_COUNT = 15
        ui.tableWidget.setColumnCount(COLUMN_COUNT)

        headers = ["Occurences", "Champions"]
        for i in range(2, COLUMN_COUNT):
            headers.append("")
            
        ui.tableWidget.setHorizontalHeaderLabels(headers)

        if checkboxes["euw"]:
            considered_regions.update({"euw" : euw_comps})

        if checkboxes["kr"]:
            considered_regions.update({"kr" : kr_comps})

        # loop over every considered region
        counter = 0
        for region in considered_regions:

            # initialize filter dictionary with following shape
            filters={"traits"   : {},
                    "champions" : {},
                    "placements": [] 
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

            # loop over compisitiongroups of each region
            for composition_group in filtered_composition_groups:
                
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
                    # add the elements into the table
                    current = QTableWidgetItem(str(champion.name))
                    ui.tableWidget.setItem(counter, keycounter, current)

                    keycounter = keycounter + 1

                counter = counter + 1

    #############################################################################
    def items_button_pressed():
        print("Work in Progress")

    #############################################################################
    def load_data_button_pressed():
        # to modify outer variables in inner function
        nonlocal euw_comps
        nonlocal kr_comps
        nonlocal euw_loaded
        nonlocal kr_loaded

        # verify which checkboxes are pressed or not pressed
        checkboxes = {  "euw":  ui.euwCheckBox.isChecked(),
                        "kr":   ui.krCheckBox.isChecked()}

        if not checkboxes["euw"] and not checkboxes["kr"]:
            return

        if checkboxes["euw"] and not euw_loaded:
            europe = get_compositions(  region="europe",
                                        games_per_player=4,
                                        players_per_region=5,
                                        current_patch=ui.currentPatchFilter.text())     

            # sort composition group on occurences
            euw_comps_unsorted = group_compositions_by_traits(europe)
            euw_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)
            euw_comps = sorted(euw_comps_unsorted, key=lambda x: x.counter, reverse=True)

            euw_loaded = True
            ui.euwCheckBox.setStyleSheet("color: green;")

        if checkboxes["kr"] and not kr_loaded:
            korea = get_compositions(   region="korea",
                                        games_per_player=4,
                                        players_per_region=5,
                                        current_patch=ui.currentPatchFilter.text())
            
            # sort composition group on occurences
            kr_comps_unsorted = group_compositions_by_traits(korea)
            kr_comps_unsorted.sort(key=lambda x: x.counter, reverse=True)
            kr_comps = sorted(kr_comps_unsorted, key=lambda x: x.counter, reverse=True)

            kr_loaded = True
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

    # bind functions to the buttons
    ui.compositionsButton.clicked.connect(compositions_button_pressed)
    ui.traitsButton.clicked.connect(traits_button_pressed)
    ui.championsButton.clicked.connect(champions_button_pressed)
    ui.itemsButton.clicked.connect(items_button_pressed)
    ui.loadDataButton.clicked.connect(load_data_button_pressed)

    # add traits to dropdown filters
    ui.traitFilter1.addItems(CURRENT_SET_TRAITS)
    ui.traitFilter2.addItems(CURRENT_SET_TRAITS)
    ui.traitFilter3.addItems(CURRENT_SET_TRAITS)
    ui.traitFilter4.addItems(CURRENT_SET_TRAITS)

    # setup the other guis
    popup_window = QMainWindow()
    popup = composition_group_view.Ui_compositionGroupView()

    main_window.show()
    app.exec_()


run_main_gui()