class kwRepository {
    constructor(data){
        if(data["name"]){
            this.name = data["name"];
        } else {
            this.name = "Enter Repository Details"
        }
        this.url = data["@url"];
        this.label = data["@label"];
        this.clone = data["@clone"].toLowerCase().trim();
        this.all_drivers = data["@all_drivers"].toLowerCase().trim();
        this.available = data["available"];
        this.drivers = [];
        for(var i=0; i<data["driver"].length; i++){
            this.drivers.push(new driverDetails(data["driver"][i]));
        }
    }

    addDriver(name, clone){
        this.drivers.push(new driverDetails(name, clone))
    }

    get domElement(){
        return this.formDomElement();
    }

    formDomElement() {
        var clone_icon = "fa fa-toggle-off grey";
        if(this.clone == "yes"){
            clone_icon = "fa fa-toggle-on green";
        }
        var available_icon = "fa fa-times red";
        var available_text = "Repository Not Available"
        if(this.available){
            available_icon = "fa fa-check-circle green"
            available_text = "Repository Available"
        }
        var hideAvailability = "";
        if(this.url == ""){
            hideAvailability = "display: none";
        }
        var driverDom = '';
        for(var i=0; i<this.drivers.length; i++){
            driverDom = driverDom + this.drivers[i].domElement;
        }
        var displayDrivers = "";
        if(driverDom == ""){
            displayDrivers = "display: none";
        }
        var allDriversIcon = "fa fa-toggle-off grey";
        if(this.all_drivers == "yes"){
            allDriversIcon = "fa fa-toggle-on green";
        }
        var $elem =  $('<div class="card" style="padding: 1rem;">' +
                            '<div class="card-header">' +
                                '<div class="row">' +
                                    '<div class="col-sm-1">' +
                                        '<i class="' + clone_icon + '" style="float:right; line-height:inherit!important;" ' +
                                            'aria-hidden="true" katana-click="assembler.toggleKwRepoClone" aria-selected="true"></i>' +
                                    '</div>' +
                                    '<div class="col-sm-8">' +
                                        this.name +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="card-block" style="padding: 1rem;">' +
                                '<div class="row">' +
                                    '<div class="col-sm-1" style="text-align: right; padding: 0.7rem;">' +
                                        '<label>URL:</label>' +
                                    '</div>' +
                                    '<div class="col-sm-5">' +
                                        '<input value="' + this.url + '" katana-change="assembler.updateKwRepoDetails">' +
                                    '</div>' +
                                    '<div class="col-sm-1" style="text-align: right; padding: 0.7rem;">' +
                                        '<label>Label:</label>' +
                                    '</div>' +
                                    '<div class="col-sm-3">' +
                                        '<input value="' + this.label + '">' +
                                    '</div>' +
                                '</div>' +
                                '<div class="row" style="' + displayDrivers + '">' +
                                    '<div class="col-sm-1"></div>' +
                                    '<div class="col-sm-9">' +
                                        '<div class="card">' +
                                            '<div class="card-header">' +
                                                '<i class="' + allDriversIcon + '"></i>' +
                                                '<label>All Available Drivers</label>' +
                                            '</div>' +
                                            '<div class="card-block" style="padding: 1rem;">' +
                                                '<div class="row text-center">' +
                                                    driverDom +
                                                '</div>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                '</div>'+
                                '<br>' +
                            '</div>' +
                            '<div class="card-footer">' +
                                '<div class="row" style="' + hideAvailability + '">' +
                                    '<div class="col-sm-1">' +
                                        '<i class="' + available_icon + '" style="float:right; line-height:inherit!important;"></i>' +
                                    '</div>' +
                                    '<div class="col-sm-8 text-muted">' +
                                        available_text +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                        '<br>');
        return $elem;
    }

    get jsonObj() {
        return this.formJsonObj();
    }

    formJsonObj(){
        var driversJson = [];
        for(var i=0; i<this.drivers; i++){
            driversJson.push(drivers[i].jsonObj)
        }
        var jsonObject = {
            "@url": this.url,
            "@label": this.label,
            "@clone": this.clone,
            "@all_drivers": this.all_drivers,
            "driver": driversJson
        }
        return jsonObject;
    }

}

class driverDetails {
    constructor(data){
        this.name = data["@name"];
        this.clone = data["@clone"];
    }

    get domElement(){
        return this.formDomElement();
    }

    formDomElement() {
        if(this.name){
            var clone_icon = "fa fa-toggle-off grey";
            if(this.clone == "yes"){
                clone_icon = "fa fa-toggle-on green";
            }
            var elem = '<div class="col-sm-4">' +
                            '<i class="' + clone_icon + '"></i>' +
                            '<label>' + this.name + '</label>' +
                        '</div>';
        }
        else{
            var elem = "";
        }

        return elem;
    }

    get jsonObj() {
        return this.formJsonObj();
    }

    formJsonObj(){
        var jsonObject = {
            "driver": {
                "@name": this.name,
                "@clone": this.clone
            }
        }
    }
}

class wsRepository {
    constructor(url, label, clone, overwrite){
        this.url = url;
        this.clone = clone;
        this.label = label;
        this.overwrite = overwrite;
    }

    get domElement(){
        return this.formDomElement();
    }

    formDomElement() {
        var html_contents = "";
        var $elem = $(html_contents);
        return $elem
    }

    get jsonObj() {
        return this.formJsonObj();
    }

    formJsonObj(){
        var jsonObject = {
            "@url": this.url,
            "@label": this.label,
            "@clone": this.clone,
            "@overwrite": this.overwrite,
        }
        return jsonObject;
    }
}

class dependency{
    constructor(data){
        this.name = data["@name"];
        this.install = data["@install"].toLowerCase().trim();
        this.user = data["@user"].toLowerCase().trim();
        this.version = data["version"];
        this.installed = data["installed"];
        this.matched = data["matched"];
    }

    get domElement(){
        return this.formDomElement();
    }

    formDomElement() {
        var installed_btn = '<button class="btn btn-success" ' +
                                     'katana-click="assembler.installDependency" ' +
                                     'aria-selected="false">' +
                                         'Install' +
                            '</button>';
        var available_txt = '<h6 class="card-subtitle mb-2 text-muted">&nbsp;</h6><br>';
        if(this.installed){
            available_txt = '<h6 class="card-subtitle mb-2 text-muted">' +
                                'Available Version: ' + this.installed +
                            '</h6><br>';
            if(!this.matched){
                installed_btn = '<button class="btn btn-danger" ' +
                                         'katana-click="assembler.installDependency" ' +
                                         'aria-selected="false">' +
                                             'Install' +
                                '</button>';
            }
            else if(this.matched == "lower"){
                installed_btn = '<button class="btn btn-info" ' +
                                         'katana-click="assembler.upgradeDependency" ' +
                                         'aria-selected="false">' +
                                             'Upgrade&nbsp;' +
                                             '<i class="fa fa-exclamation-triangle tan" ' +
                                                 'aria-hidden="true">' +
                                             '</i>&nbsp;' +
                                '</button>';
            }
            else if(this.matched == "higher"){
                installed_btn = '<button class="btn btn-success">' +
                                    'Installed&nbsp;' +
                                    '<i class="fa fa-check-circle green" aria-hidden="true"></i>' +
                                    '&nbsp;' +
                                '</button>';
            }
            else{
                installed_btn = '<button class="btn btn-success">' +
                                    'Installed&nbsp;' +
                                    '<i class="fa fa-check-circle green" aria-hidden="true"></i>&nbsp;' +
                                '</button>';
            }
        }

        var html_contents = '<div style="padding: 1rem;">' +
                                '<div class="card" style="width: 350px; height:190px; padding: 1rem;">' +
                                    '<div class="card-block">' +
                                        '<h4 class="card-title">' + this.name +'</h4>' +
                                        '<h6 class="card-subtitle mb-2 text-muted">Version: ' + this.version + '</h6><hr>' +
                                        available_txt +
                                        installed_btn +
                                    '</div>' +
                                '</div>' +
                            '</div>'
        var $elem = $(html_contents);
        return $elem
    }

    get jsonObj() {
        return this.formJsonObj();
    }

    formJsonObj(){
        var jsonObject = {
            "@name": this.name,
            "@install": this.install,
            "@user": this.user,
        }
        return jsonObject;
    }
}