/*
order of sections for the .js file. - if you search /section it will take you to the tops of the sections
1. data - variables used in the react/vue component
2. mounting,destroying, creating
3. fetching
4.modal function/handlers
5. employee log in/out functions
6. open/close table and table handling
7. add order,clear order,remove item, print order, 
8. editing .json/flask

*/
const Order = {
    delimiters: ['[[', ']]'],
    data() {//////////////////////////////////////Section data
        return {
            tables: [],
            butNums: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'CLR', 'DEL', 'OK', "X"],
            currentTableId: 0,
            menu_items: [],
            menus: [],
            menu_sections: [],
            toppings: [],
            entreChoice: [],
            indTotal: 0,
            overallTotal: 0,
            finalOrder: [],
            finalOrderItems: [],
            sel_menu: 0,
            sel_section: 0,
            txaFinalOrder: '',
            empPin: '',
            empName: '',
            empHours: 0,
            userEnterVal: '',
            clockVal: -1,
            seatTableCheck: -1,
            noStock: [],
            tip15: 0,
            tip20: 0,
            tip25: 0,
            waittime: 0,

        }//end return
    }, //end data property

    // I looked into using socket.io for polling for updates for the webpage.
    /* It occured to me that since we are using Flask to run the server for the website, it is cleaner to 
        using a socket to tell the website when to poll the JSON files for updates. It is real easy to understand
        and as with everything Python, there is a module to make it easy to use. The basic idea is that instead of 
        polling every 3 seconds, we create a socket to listen for a update message. Once it is it is created, we can just send 
        an update to the route, say from the back-end, telling the server that the JSON files have new data. 
    */
    mounted() {/////////////////////////////////////Section mount,destroy, create
        // Create the socket
        this.socket = io('http://localhost:5000');

        // When it is created, in console lets us know
        this.socket.on('connect', () => {
            console.log('Connected to WebSocket server!');
        });

        // Here is where it is listening for message and runs the fetchData, which just loads the data from th JSON files
        this.socket.on('JSON_Update', () => {
            //console.log(data.message);
            this.fetchData();
        });
    },

    created() {
        /* get the entres from the file written from the database */
        this.fetchData();
    },
    beforeDestroy() {
        if (this.socket) {
            this.socket.disconnect();
        }
    },

    methods: {
        // All of the JSON files are fetched and data is filled
        // Called when new data is in the JSON files
        fetchData() {////////////////////////////////////Section fetch
            fetch('./static/data/menu_items.json')
                .then(response => response.json())
                .then(data => {
                    this.menu_items = data.menu_items;
                    //if the menu item has a stock of 0 or below we want to add it to the array to display in the text area
                    for (let i = 0; i < this.menu_items.length; i++) {
                        if (this.menu_items[i].menu_item_stock <= 0) {
                            //add that element to the array
                            if (!this.noStock.includes(this.menu_items[i].menu_item_name))
                                this.noStock.push(this.menu_items[i].menu_item_name)

                        }

                    }
                    for (let j = 0; j < this.noStock.length; j++) {
                        if (this.noStock[j] <= 0) {
                            //add that element to the array
                            document.getElementById(this.noStock[j]).style.color = red

                        }

                    }
                    // console.log("nostock " + this.noStock)
                })
            fetch('./static/data/menu.json')
                .then(response => response.json())
                .then(data => {
                    this.menus = data.menu;


                })
            fetch('./static/data/menu_sections.json')
                .then(response => response.json())
                .then(data => {
                    this.menu_sections = data.menu_sections;
                })
            /* read the toppings from a new .json file */
            fetch('./static/data/toppings.json')
                .then(response => response.json())
                .then(data => {
                    this.toppings = data.toppings;
                })
                .catch(function (error) {
                    console.log(error);
                })
            fetch('./static/data/table_orders.json')
                .then(response => response.json())
                .then(data => {
                    this.tables = data.tables;
                })
        },
        ////////////////////////////////////////////SECTION Modal Handlers

        /* This one function is used to handle all inputs of the buttonModal, it loads the buttons from the VUE
            data and takes the input of what button was pressed. 
        */
        async handleBtn(btnum) {

            // The `X` button clears all VUE data that is associated with trying to LogIn and hides the modal
            if (btnum == "X") {
                this.userEnterVal = ""
                this.empPin = ''
                this.empName = ''
                this.clockVal = -1
                document.getElementById("buttonModal").style.display = "none"
            }

            // The `CLR` button just clears what was entered by the employee
            else if (btnum == "CLR") {
                this.userEnterVal = ""
            }

            // The `DEL` button just removes the last number entered 
            else if (btnum == "DEL") {
                let empStr = this.userEnterVal
                empStr = empStr.slice(0, -1)
                this.userEnterVal = empStr
            }

            /* The `OK` button is a little more complex. If we are clicked the employee logIn button, we then are just going to 
                go down the path of clocking In. If we click a table button, the button modal is called, however, here it will check
                to see if `seatTableCheck` is positive, which means we are trying to seat a table and possibly logIn. This calls a different 
                function from the normal employee login.
            */
            else if (btnum == "OK") {
                if (this.seatTableCheck == -1) {
                    this.handleEmplLog()
                    document.getElementById("buttonModal").style.display = "none"
                }
                else {
                    this.handleTableSeat()
                    document.getElementById("buttonModal").style.display = "none"
                }

            }
            // Here is checks to see if are `empPin` is empty, that means we are trying to enter our 3 digit pin number
            // This just updates `userEnterVal`, which is displayed in the button modal
            else if (this.userEnterVal.length != 3 && this.empPin == '') {
                this.userEnterVal += btnum
            }

            // Same thing, but now we are trying to enter the 4 digit password
            else if (this.userEnterVal.length != 4 && this.empPin != '') {
                this.userEnterVal += btnum
            }
            // Nothing happens here
            else {

            }
        },
        /* Here is the modal type that is used with everything realated to performing a regular logIn/logOut
                    with the employee button. the param `data` is used in the sister table modals but not really here.
                    It first grabs anythng related to the employee modal and makes two const when called are used to hide
                    all modal objects and clear the values realted to employee logIn/LogOut.
                */
        async modalTypeLogin(type, data = 0) {

            const buttonModal = document.getElementById("buttonModal")
            const myModalAsk = document.getElementById("myModalAsk")
            const askModal = document.getElementById("askModal")
            const btn_LogYes = document.getElementById("btn_LogYes")
            const btn_LogBack = document.getElementById("btn_LogBack")
            const btn_LogCancel = document.getElementById("btn_LogCancel")
            const h_Ask = document.getElementById("h_Ask")

            const hideAll = () => {
                btn_LogYes.style.display = 'none'
                btn_LogBack.style.display = 'none'
                btn_LogCancel.style.display = 'none'
                myModalAsk.style.display = "none"
                askModal.style.display = "none"
                h_Ask.innerHTML = ''
                buttonModal.style.display = 'none'
            }

            const clrValues = () => {
                this.userEnterVal = ''
                this.empPin = ''
                this.clockVal = -1
                this.empName = ''
            }

            // By default, the modal objects are all hidden and the parent modal is displayed when this function is called
            hideAll()
            myModalAsk.style.display = 'block'

            // Found Employee
            // Called when employee is found based on `pin_num` and checks to see if they are clocked in or out
            if (type == 'F_empNum') {
                await this.check_clock()
                //(this.clockVal)
                if (this.clockVal == 0) {
                    h_Ask.innerHTML = "Log-In as " + this.empName + "?"
                }

                else if (this.clockVal == 1) {
                    h_Ask.innerHTML = "Log-Out as " + this.empName + "?"
                }
                else {
                    console.error("Clock Value")
                }
                askModal.style.display = "block"

                btn_LogYes.style.display = 'flex'
                btn_LogBack.style.display = 'flex'
                btn_LogCancel.style.display = 'flex'
            }

            // Not Found Employee
            // Called when employee is not found based on the `pin_num`
            else if (type == 'NF_empNum') {
                h_Ask.innerHTML = "No Employee found for " + this.userEnterVal

                askModal.style.display = "flex"

                btn_LogBack.style.display = 'flex'
                btn_LogCancel.style.display = 'flex'
            }

            // Successful Login
            // Called when employee successfully logIn/logOut
            else if (type == 'S_login') {

                if (this.clockVal == 0) {
                    askModal.style.zIndex = 2
                    h_Ask.innerHTML = `EMPL: ${this.empName} (${this.empPin}) \n Clocked In`
                }

                else if (this.clockVal == 1) {
                    h_Ask.innerHTML = `EMPL: ${this.empName} (${this.empPin}) \n Clocked Out <br><br> Total Hours: ${this.empHours}`
                }
                else {
                    console.error("Clock Error")
                }

                askModal.style.display = "flex"
                btn_LogCancel.style.display = 'flex'
            }

            // Invaild Employee Pin
            // Called when employee `pin_code` is invaild
            else if (type == 'NF_empPin') {
                h_Ask.innerHTML = "Invaild Pin Entered"

                askModal.style.display = "flex"

                btn_LogBack.style.display = 'flex'
                btn_LogCancel.style.display = 'flex'
            }

            // Cancel
            // Button on modals to close all and clear all values
            else if (type == 'cancel') {
                hideAll()
                clrValues()

            }

            // Back
            // Is used to go back to button modal if the option is there
            // i.e. `NF_empNum`, go back to enter a different employee number
            else if (type == 'back') {
                hideAll()

                buttonModal.style.display = "block"
            }

            // Yes
            // Used to go to the next step of the `logEmpl`
            // i.e. `F_empNum`, click yes to enter your employee code 
            else if (type == 'yes') {
                hideAll()

                this.empPin = this.userEnterVal
                this.userEnterVal = ''
                this.logEmpl()
            }
            else {
                console.error("Modal Type Login")
            }
        },
        /* Almost identical to the `modalTypeLogin`, but has a few more options related to the tables.
            Works the same way and has the same hide/clear consts in the start. A key thing is the `seatTableCheck`
            is a postive value when using these modals which means the logIn process is different.
        */
        modalTypeTable(type, data = 0) {
            const buttonModal = document.getElementById("buttonModal")
            const myModalAsk = document.getElementById("myModalAsk")
            const askTableModal = document.getElementById("askTableModal")
            const btn_TableYes = document.getElementById("btn_TableYes")
            const btn_TableBack = document.getElementById("btn_TableBack")
            const btn_TableCancel = document.getElementById("btn_TableCancel")
            const h_Ask = document.getElementById("h_Ask")

            const clrValues = () => {
                this.userEnterVal = ''
                this.seatTableCheck = -1
                this.empName = ''
                this.empPin = ''
            }
            const hideAll = () => {
                btn_TableYes.style.display = 'none'
                btn_TableBack.style.display = 'none'
                btn_TableCancel.style.display = 'none'
                myModalAsk.style.display = "none"
                askTableModal.style.display = "none"
                h_Ask.innerHTML = ''
                buttonModal.style.display = 'none'
            }

            // Hide all and display parent 
            hideAll()
            myModalAsk.style.display = 'block'

            // Closed Table
            // Shows when clicked on a closed table
            if (type == 'CL_table') {
                h_Ask.innerHTML = `Table ${data} is closed.`
                askTableModal.style.display = "flex"
                btn_TableCancel.style.display = 'flex'
            }

            // Open Table
            // Shows when clicked on a open table
            else if (type == 'OP_table') {
                h_Ask.innerHTML = `Seat Table ${data}?`
                askTableModal.style.display = "flex"
                btn_TableYes.style.display = 'flex'
                btn_TableCancel.style.display = 'flex'
            }

            // Locked Table
            // Shows when clicked on a locked table
            else if (type == 'LOCK_table') {
                myModalAsk.style.display = 'none'
                this.logEmpl()
            }

            // Reserved Table
            // Shows when clicked on a reserved table
            else if (type == 'RS_table') {
                h_Ask.innerHTML = `Table ${data} is Reserved at <br> ${this.tables[data - 1].SrtTime}.`
                askTableModal.style.display = "flex"

                btn_TableCancel.style.display = 'flex'
            }

            // Successful Table Sat
            // Shows when we have successfully sat a table
            else if (type == 'S_tableSat') {
                this.seatTable()
                h_Ask.innerHTML = ` EMPL: ${this.empPin} <br> Table ${this.seatTableCheck} has been sat.`
                askTableModal.style.display = "flex"
                btn_TableCancel.style.display = 'flex'
            }

            else if (type == 'PAID_table') {
                h_Ask.innerHTML = ` Table: ${data} <br> Has been cleared.`
                askTableModal.style.display = "flex"
                btn_TableCancel.style.display = 'flex'
            }

            // Yes
            // Used to start the LogIn process
            // A big difference is that `seatTableCheck` is a positive when we click this button
            // This means `logEmpl` will instead use the table function instead to handle a logIn
            else if (type == 'yes') {
                hideAll()
                this.userEnterVal = ''
                this.logEmpl()

            }

            // Back 
            // Same as other modal, goes back to button modall
            else if (type == 'back') {
                hideAll()
                buttonModal.style.display = "block"
            }

            // Cancel
            // Same as other modal, clears and hides all
            else if (type == 'cancel') {
                hideAll()
                clrValues()
            }

            // X-Access
            // Used to show the employee does not have access to that table
            else if (type == 'X_access') {
                askTableModal.style.display = "flex"
                h_Ask.innerHTML = `You do not have access <br> to this table!`

                btn_TableCancel.style.display = 'flex'
            }

            // Force LogIn
            // If the employee is not clocked in, offer them to logIn
            // Since `seatTableCheck` is posivitve, uses a different function
            else if (type == 'force_Login') {
                askTableModal.style.display = "block"
                h_Ask.innerHTML = `You must Log-In first. <br> Log-In as ${this.empName}?`

                btn_TableYes.style.display = 'flex'
                btn_TableBack.style.display = 'flex'
                btn_TableCancel.style.display = 'flex'
            }

        },
        ///////////////////////////////////////////SECTION employee log in functions

        // When called, runs the Back-End program from Flask
        loadAdmin() {
            fetch('/admin_BackEnd')
        },
        /* When called, clocks the Employee in or out.
                   It sends the `empPin`, the 4 digit pincode, instead of the `empCode` since we use the `check_clock` with the `empCode`
                   so that kinda checks if the `empCode` is vaild and this checks if the empPin is vaild. It also sends the `getTimestamp` which
                   is used for the clock in/out time and the `clockVal` that is used to track if they should be clocked in or out.
               */
        async clockEmpl() {
            const postData = {
                empCode: this.empPin,
                timestamp: this.getTimestamp(),
                clockVal: this.clockVal
            };
            try {
                const response = await fetch('/clock_Empl', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(postData)
                })

                // So here, it returns the hours worked and returns it to a var in the functions used to login Employee.
                const data = await response.json()
                console.log("Success:", data)
                return data['Contents']

            } catch (error) {
                console.error("Error: ", error)
            }
        },

        /* The function here takes the `empCode` and sends it to Flask to check if the employee is clocked in/out
            The `userEnterVal` is the value that is entered with the employee login button modal. This is used multiple times
            to hold both the `empCode` and `empPin`
        */
        async check_clock() {
            const postData = {
                empCode: this.userEnterVal,
            };
            try {
                const response = await fetch('/check_clock', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(postData)
                })

                // Here it returns the value used to check if the employee is clocked in or out
                const data = await response.json()
                this.clockVal = data
                console.log(this.clockVal)
                console.log('Success:', data);

            } catch (error) {
                console.error('Error', error)
            }
        },
        logEmpl() {
            if (this.empPin != '') {
                document.getElementById("buttonHead").innerHTML = "Enter Employee Pin"
                document.getElementById("buttonModal").style.display = "block"
            }
            else if (this.empPin == '') {
                document.getElementById("buttonHead").innerHTML = "Enter Employee Number"
                document.getElementById("buttonModal").style.display = "block"
            }
            else {
                console.error("Emp Login")
            }
        },
        /* When called, this takes a param and looks at the employee json for that employee. It is used both when looking for an
                    employee by the `empPin` and the `empCode`. It returns if it finds an employee or if none was found.
                */
        async findEmployee(param) {
            const response = await fetch('./static/data/employees.json');
            const data = await response.json()

            // The param is the `pin_code` or the `pin_num
            // I made it a seperate function in the case that we need to access employess by other params
            const employee = data.Employee.find(emp => emp[param] === parseInt(this.userEnterVal));

            return employee
        },

        /* So here is the function that is used when an employee is trying to logIn/logOUt with the employee button.
            It is called twice to check the `empPin` and then check if the `empCode` is vaild. It works with the
            function `modalTypeLogin` to display the info to the employee through the modal.
        */
        async handleEmplLog() {

            // First we check to see if the employee is a step one (entering there 3 digit id)
            if (this.empPin == '') {

                // If so, pass the `pin_num` to `findEmployee` and wait for a response
                const employee = await this.findEmployee('pin_num')

                // If we find an employee, we store there name and make the modal that asks them if the want to logIn/logOut
                // The check for if they we offer them to logIn or logOut is done in the modal
                if (employee) {
                    this.empName = employee.display_name
                    this.modalTypeLogin('F_empNum')
                }

                // If we don't find an employee with the `pin_num` entered, we let them know and clear out the stored `empPin`
                // This is done to prevent the modal asking for the `pin_code` being prompted
                else {
                    this.empPin = ""
                    this.modalTypeLogin('NF_empNum')
                }
            }

            // If we are at step 2 (Asking them for the 4 digit pass)
            else if (this.empPin != '') {

                // If so, pass the `pin_code` to `findEmployee` and wait for a response
                const employee = await this.findEmployee('pin_code')

                // If we find an employee, we then logIn or logOut and show the modal, the `empHours` is what is returned during for logOut
                if (employee) {
                    this.empHours = await this.clockEmpl()
                    //console.log(this.empHours)
                    this.modalTypeLogin('S_login')
                }

                // If they enter the wrong pin, display the modal letting them know
                else {
                    this.modalTypeLogin('NF_empPin')
                }
            }
        },





        /////////////////////////////////////////SECTION open/close tables
        /* this function helps close the table when the button is clicked to close a table */
        async closeTable() {
            const tableToClose = this.tables[this.currentTableId - 1];
            // Check if there's a server assigned to the table
            if (tableToClose.server != "") {
                // Unlock the table by removing the server number and setting status to open
                //also want to clear all the data inside the order box
                //need to print before clearing or nothing will come out of it
                this.printOrder()
                tableToClose.server = "";
                tableToClose.SrtTime = ""
                this.clearOrder()
                this.finalOrder = ""
                tableToClose.status = 'open';
                //prints recipt to alert


                this.modalTypeTable('PAID_table', this.currentTableId)
                this.lockTable()

                // Update the table information
                this.updateTableOrdersFlask(); // Call to update Flask
            } else {
                console.log("No server assigned to this table.");
            }
        },
        /* This function is used to set the style of each of the table buttons in the HTML window. In short, using VUE,
                   when looping to create the table buttons, it here sets the style of each one based on the status. The return of 
                   each case refers to each type of style in the CSS file. 
               */

        tableCheck(table) {
            switch (table.status) {
                case 'open':
                    return 'tableAval'
                case 'close':
                    return 'tableClose'
                case 'resv':
                    return 'tableRes'
                case 'lock':
                    return 'tableLock'
                default:
                    console.error(`Table Style Error: Style: ${table.status}`)
            }
        },

        /* With switching tables, this is called first to get the status of the table that the employee is trying to go into.
            It uses the `tableId` of the table clicked on makes a quick check of the status of the table. The `seatTableCheck` is
            used to keep track of what index table we are interacting with. This made it easier to have it check if when an employee
            is trying to logIn, is it a normal logIn or a logIn with tables.
        */
        getTableStatus(tableId) {
            const tableStatus = this.tables[tableId - 1].status
            this.seatTableCheck = tableId

            // Opens the function `modalTypeTable` that displays the options that are avaible with that table status
            switch (tableStatus) {
                case 'open':
                    this.modalTypeTable('OP_table', tableId)
                    break;
                case 'close':
                    this.modalTypeTable('CL_table', tableId)
                    break;
                case 'lock':
                    this.modalTypeTable('LOCK_table', tableId)
                    break;
                case 'resv':
                    this.modalTypeTable('RS_table', tableId)
                    break;
                default:
                    console.error("Table get Status")
            }
        },

        // This is used when pressing the exit button on the table display to manulally lock a table
        lockTable() {
            this.currentTableId = 0
            this.seatTableCheck = -1
            this.finalOrder = ''
            this.overallTotal = ''
            this.indTotal = ''
            this.checkWait()

        },
        /*
        check and update the wait time
        if all the tables are taken we have a base time of an hour. 
        if any are open the time should be 0 minutes
        */
        checkWait() {
            let open_tables = this.tables.length
            for (let i = 1; i < this.tables.length; i++) {
                if (this.tables[i].status != 'open') {
                    open_tables--
                }
            }
            //all the tables are full --> wait time 60 minutes
            if (open_tables == 0) {
                this.waittime = 60
            }
            else {
                this.waittime = 0
            }
        },

        /* So this was orignally called when a table button was pressed, however with the table status options, there
            had to be a few checks before switching a table. It takes the `tableId` of the one we want to open, and also
            looks at the table that we are switching from. */
        switchTable(tableId) {
            this.checkWait() // updates the wait time
            const tableSwitchFrom = this.tables.find(table => table.id === this.currentTableId);
            console.log(tableSwitchFrom)

            // This is if we are not in a table screen, it just has to pull the data of the table we want to go to 
            // If we don't check if a table is NULL, we would get an error when trying `tableSwitchFrom.id` 
            if (!tableSwitchFrom) {
                console.log("No table on window")
                //console.log(this.tables)
                const tableSwitchTo = this.tables.find(table => table.id === tableId);

                this.currentTableId = tableSwitchTo.id
                this.finalOrder = tableSwitchTo.tableOrder
                this.overallTotal = tableSwitchTo.tableTotal
            }

            // If we click the table we currently have open, we are not going to do anything
            else if (tableSwitchFrom.id == tableId) {
                //console.log("same table switch")
                return
            }

            // When we go to a new table with a table open, similar to if there is no table open at all
            else {
                // console.log(this.tables)
                const tableSwitchTo = this.tables.find(table => table.id === tableId);

                this.currentTableId = tableSwitchTo.id
                this.finalOrder = tableSwitchTo.tableOrder
                this.overallTotal = tableSwitchTo.tableTotal.toFixed(2)
            }

        },

        /* Called when when have made it through all the steps with creating an open table. It gets the table to seat
            by the `seatTableCheck`, but we need the index of the table not the id so we minus 1. I also found the 
            simple solution to the problem of calling this function with checking the `empCode` or `empPin`, to just run
            another check if one of them returns NULL. 
        */
        async seatTable() {
            const tableToSeat = this.tables[this.seatTableCheck - 1]
            //console.log(tableToSeat)

            // So here I ran into trouble with checking the `pin_num` and the `pin_code`
            // In the `findEmployee`, it uses the last value the employee entered in the buttonModal, `userEnterVal`
            // If you are clocked in, you just need the pin, if not, it uses the code
            let server = await this.findEmployee('pin_num')
            if (!server) {
                server = await this.findEmployee('pin_code')
            }
            //console.log(server)

            // Fills the `tables` that is beaing seated with all data and locks it to that employee
            tableToSeat.server = server['pin_num']
            tableToSeat.SrtTime = this.getTimestamp()
            tableToSeat.status = 'lock'

            this.switchTable(this.seatTableCheck)   // Now we can switch to that table we just locked to the employee
            this.updateTableOrdersFlask()   // Call to update Flask
        },
        // This function is used to return the full table info from the `tables` based on the `seatTableCheck`
        // Used when neededing to check the status of the table during logIn
        async checkTableData() {
            const tableData = this.tables.find(tb => tb['id'] === parseInt(this.seatTableCheck));
            console.log("table Data: " + tableData)
            return tableData

        },

        /* This function is called when the employee clicks on the table buttons and trys to seat a table. It handles an 
            employee trying to open a table, access a locked table, and logIn an employee if they are not already before 
            seating a table. It works closely with the function `modalTypeTable` to display the modals realted to tables.
        */
        async handleTableSeat() {

            // Gets data about the table we are interacting with
            const tableData = await this.checkTableData()

            //If the table we are trying to go into is open
            if (tableData['status'] == 'open') {

                // If are `empPin` is empty
                // This is here because this function is also use to logIn employess
                // So similar to `handleEmplLog` we check to see what logIn part they are at (code or pass)
                if (this.empPin == '') {

                    // Check for employee with `pin_num`
                    const employee = await this.findEmployee('pin_num')

                    // We dont find an employee, open modal saying not found
                    if (!employee) {
                        this.modalTypeLogin('NF_empNum')
                    }

                    // We find them, but they do not have access, we don't let them do anything
                    else if (employee.access_level > 2) {
                        this.modalTypeTable("X_access")
                        return
                    }

                    // We find an employee and they have access, we check to see if they are clocked in and update `clockVal` based on that
                    else {
                        await this.check_clock()

                        // They are not clocked in, offer them to clock in
                        if (this.clockVal == 0) {
                            this.empPin = this.userEnterVal
                            this.empName = employee.display_name
                            this.modalTypeTable("force_Login")
                        }

                        // They are clocked in, the table is then sat
                        else {
                            this.empPin = this.userEnterVal
                            this.empName = employee.display_name
                            this.modalTypeTable("S_tableSat")
                        }
                    }
                }

                // Here is part 2 of the logIn process the same as part 2 of employee login but handled here for tables
                else if (this.empPin != '') {
                    const employee = await this.findEmployee('pin_code')
                    if (!employee) {
                        this.modalTypeLogin('NF_empPin')
                    }

                    // Difference is we clock them in and seat the table
                    else if (employee) {
                        this.empHours = await this.clockEmpl()
                        this.modalTypeTable("S_tableSat")

                    }
                }
            }

            // If the table we clicked is locked
            else if (tableData['status'] == 'lock') {

                // Lookup employee based on `pin_num`
                const employee = await this.findEmployee('pin_num')

                // If it does not match the one in the tables data, they dont have access
                if (!employee || employee['pin_num'] != tableData['server']) {
                    this.modalTypeTable("X_access")
                }

                // Else, they do have access and we switch the table
                else if (employee) {
                    console.log(employee)
                    this.switchTable(this.seatTableCheck)
                    this.userEnterVal = ''
                }
            }

        },



        ////////////////////////////////////////SECTION add,remove, clear, print, 
        /* calculate the cost of each individual item so it is easier to add to the overall bill */
        calc() {
            //alert("HI");
            this.indTotal = 0;
            if (this.entreChoice) {
                this.indTotal = this.entreChoice.menu_item_price;
            }
            this.indTotal = parseFloat(this.indTotal).toFixed(2);
        },//end Calc 
        /* adds the input to the final order display. this function is like sending something to the 
        check. */
        addToFinal() {
            if (this.noStock.includes(this.entreChoice.menu_item_name)) {
                alert("We ran out of " + this.entreChoice.menu_item_name + ". Please select a different item.")
            }
            else {
                if(this.entreChoice.menu_item_name) {
                    this.updateItemStockFlask(this.entreChoice.menu_items_id, this.entreChoice.menu_item_stock) // Call for Flask update
                    this.finalOrder += this.entreChoice.menu_item_name + " "
                    this.sentToPrinters()
                    this.entreChoice = []
                    //console.log(this.entreChoice)
                    this.overallTotal = parseFloat(this.overallTotal) + parseFloat(this.indTotal)
                    this.finalOrder += this.indTotal
                    this.finalOrder += "\n"
                    this.overallTotal = this.overallTotal.toFixed(2)
                    this.tables[this.currentTableId - 1]['tableOrder'] = this.finalOrder
                    this.tables[this.currentTableId - 1]['tableTotal'] = this.overallTotal
                    this.entreChoice = []
                    this.updateStock("subtract_from_stock")
                    this.updateTableOrdersFlask() // Call for Flask update
        
                }
                else {
                    console.error("Final Order: No item selected")
                }
            }
        },
        sendToPrinters() {
            if (this.entreChoice.menu_item_parent == 1) {
                console.log("Grill: " + this.entreChoice.menu_item_name);
            } else if (this.entreChoice.menu_item_parent == 2) {
                console.log("Salad station: " + this.entreChoice.menu_item_name);
            } else if (this.entreChoice.menu_item_parent == 3) {
                console.log("Appetizer station: " + this.entreChoice.menu_item_name);
            } else if (this.entreChoice.menu_item_parent == 4) {
                console.log("Wraps: " + this.entreChoice.menu_item_name);
            } else if (this.entreChoice.menu_item_parent == 5) {
                console.log("Main grill: " + this.entreChoice.menu_item_name);
            } else if (this.entreChoice.menu_item_parent == 6) {
                console.log("front of house: " + this.entreChoice.menu_item_name);
            } else {
                console.error(`Kitchen Printer error`);
            }
        },
        // This function is used to clear the order
        clearOrder() {
            const currentTable = this.tables.find(table => table.id === this.currentTableId);
            currentTable.tableOrder = ''
            currentTable.tableTotal = 0
            this.finalOrder = "";
            this.indTotal = 0;
            this.overallTotal = (0).toFixed(2);
        },
        //removes specific item from the order - calls function to increment the stock as well
        removeFromFinal(tableId) {
            if (this.finalOrder.includes(this.entreChoice.menu_item_name)) {
                this.finalOrder = this.finalOrder.replace(this.entreChoice.menu_item_name, "");
                this.finalOrder = this.finalOrder.replace(parseFloat(this.entreChoice.menu_item_price).toFixed(2), "")
                this.overallTotal = this.overallTotal - this.entreChoice.menu_item_price
                this.overallTotal = this.overallTotal.toFixed(2)
                alert(this.entreChoice.menu_item_name + " was removed from the check");
                this.switchTable(this.currentTableId);
                this.updateStock("add_to_stock")
            }
            else {
                alert(this.entreChoice.menu_item_name + " was not found on this check")
            }
        },
        tip() {
            total = this.overallTotal
            this.tip15 = total * .15
            this.tip20 = total * .2
            this.tip25 = total * .25
            this.tip15.toFixed(2)
            this.tip20.toFixed(2)
            this.tip25.toFixed(2)
            tipString = "15%: " + this.tip15.toFixed(2) + "\n" + "20%: " + this.tip20.toFixed(2) + "\n" + "25%: " + this.tip25.toFixed(2)
            return (tipString)
        },

        /* our version of "printing" the recipt for the customer */
        printOrder() {
            let printable = "Final Order\n" + this.finalOrder + "\n" + " Your Total Is: $" + this.overallTotal +
                "\n\n Suggested Tips" + "\n" + this.tip() + "\n";
            alert(printable)
        },
        ///////////////////////////////////////SECTION edit .json/flask
        // When called, sends `tables` over to Flask to update the JSON file
        updateTableOrdersFlask() {
            fetch('/update_tables', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.tables)
            })
                .then(response => response.json())
                .then(data => {
                    //console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        },

        // When called, sends `menu_items` over to Flask to update the JSON file
        async updateItemStockFlask(item_id, stock) {
            console.log(item_id)
            const postData = {
                item_id: item_id,
                stock: stock,
            };
            try {
                const response = await fetch('/update_stock', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(postData)
                })

                const data = await response.json()
                console.log('Success:', data);

            } catch (error) {
                console.error('Error', error)
            }
        },
        // Each time item is added to final order, its stock is calculated
        updateStock(action) {
            if (action == 'subtract_from_stock') {
                for (let i = 0; i < this.menu_items.length; i++) {
                    if (this.finalOrder.includes(this.menu_items[i].menu_item_name)) {
                        this.menu_items[i].menu_item_stock -= 1
                        if (this.menu_items[i].menu_item_stock <= 0 && !this.noStock.includes(this.menu_items[i].menu_item_name)) {
                            this.noStock.push(this.menu_items[i].menu_item_name)
                            alert("That was the last of " + this.menu_items[i].menu_item_name)
                            document.getElementById(this.menu_items[i].menu_items_id).disabled = 'true'
                        }
                        else if (this.menu_items[i].menu_item_stock <= 0) {
                            alert("There is no more " + this.menu_items[i].menu_item_name + " in stock.")
                        }
                    }
                }
            }
            else if (action == 'add_to_stock') {
                for (let i = 0; i < this.menu_items.length; i++) {
                    if (this.menu_items[i].menu_item_name == this.entreChoice.name) {
                        this.menu_items[i].menu_item_stock += 1
                        console.log("works")
                        if (this.noStock.includes(this.menu_items[i].menu_item_name)) {
                            this.noStock.pop(this.menu_items[i].menu_item_name)
                        }
                    }
                }

            }

        },

        // Updates style based on stock
        stockCheck(stock) {
            if (stock == null) {
                return ''
            }
            else if(stock.menu_item_stock == 0) {
                try {
                    const itemRadioBtn = document.getElementById(stock.menu_items_id)
                    itemRadioBtn.disabled = true
                    return 'noStock'
                } catch (TypeError) {
                    return ''
                }   
                
            }
            else if(stock.menu_item_stock <= 5) {
                return 'lowStock'
            }
            else {
                try {
                    const itemRadioBtn = document.getElementById(stock.menu_items_id)
                    itemRadioBtn.disabled = false
                    return 'hasStock'
                } catch (TypeError) {
                    return ''
                }   
                
            }

        },
        toDatabase() {
            // Create a JSON object representing the orders data
            const ordersData = {
                tables: this.tables.map(table => ({
                    id: table.id,
                    orders: table.orders.map(order => ({
                        finalOrder: order.finalOrder,
                        overallTotal: order.overallTotal
                    }))
                })),
                //gives the time stamp for when the order is sent to the .json file
                time: this.getTimestamp()
            };
            // Convert the JSON object to a JSON string
            const jsonData = JSON.stringify(ordersData, null, 2);
            // Log jsonData to check if it's formatted correctly
            // console.log("jsonData:", jsonData);

            // Save the JSON string to a file
            const filename = 'orders.json';
            const blob = new Blob([jsonData], { type: 'application/json' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = filename;
            link.click();
            //console.log(this.getTimestamp())
        },

        getTimestamp() {
            const date = new Date();
            const month = String(date.getMonth() + 1).padStart(2, '0'); // Adding 1 because getMonth() returns zero-based month
            const day = String(date.getDate()).padStart(2, '0');
            const year = date.getFullYear();
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            const seconds = String(date.getSeconds()).padStart(2, '0');
            /* proves that it works with the console to verify the answer */
            console.log(`${year}-${month}-${day} ${hours}:${minutes}:${seconds}`)
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        }

    }//end Methods

} //end Order

Vue.createApp(Order).mount('#vueRadio')
