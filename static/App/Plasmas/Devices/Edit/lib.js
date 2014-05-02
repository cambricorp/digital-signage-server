Ink.createModule('App.Plasmas.Devices.Edit', '1', ['App.Plasmas', 'App.Plasmas.DataProvider', 'Ink.Data.Binding_1', 'Ink.UI.Aux_1'], function(app, provider, ko, inkAux) {
    var Module = function(modal) {
        var self = this;

        this.modal = modal;
        this.params = modal.params;

        this.editMode = (!!this.params.device);
        
        this.playlists = ko.observableArray();
        
        this.device = (this.params.device?inkAux.clone(this.params.device):undefined);
        
        this.macAddress = ko.observable(this.device?this.device.mac_address:'').extend({
            required: true,
            pattern: {
                 message: 'Fill in with a valid mac address, please',
                 params: '^[A-Z0-9\-]{2}:[A-Z0-9\-]{2}:[A-Z0-9\-]{2}:[A-Z0-9\-]{2}:[A-Z0-9\-]{2}:[A-Z0-9\-]{2}$'
            }
        });

        this.ipAddress = ko.observable(this.device?this.device.ip_address:'');
        
        this.name = ko.observable(this.device?this.device.name:'').extend({
            required: true,
            minLength: 3
        });
        
        this.active = ko.observable(this.device?this.device.active:true);
        
        this.version = ko.observable(this.device?this.device.version:'');
        
        this.playlist = ko.observable(this.device?this.device.playlist:'').extend({
            required: true,
            minLength: 3,
            maxLength: 15,
            pattern: {
                 message: 'Only alfanumeric characters and hifens, please',
                 params: '^[a-zA-Z0-9\-]*$'
            }
        }); 
        
        modal.confirmHandler = function () {
            self.saveDevice();
        };

        modal.confirmDisabled(ko.computed(function() {
            return false;
            //return (!self.name.isValid());
        }));
        
        this.loadPlaylists();
    };
    
    Module.prototype.loadPlaylists = function() {
        var self=this;
        
        provider.listPlaylists(function(data) {
            var playlistsJSON = data.responseJSON.playlists;
            var i;
            var lists = [];
            var list;
            
            for (i=0; i<playlistsJSON.length; i++) {
                list = playlistsJSON[i];
                lists.push(list);
            }
            
            self.playlists(lists);
        });
    };

    Module.prototype.saveDevice = function() {
        var self = this;

        if (!this.device) {
            this.device = {};
        }

        this.device.name = this.name();
        this.device.mac_address = this.macAddress();
        this.device.ip_address = this.ipAddress();
        this.device.active = this.active();
        this.device.version = this.version();
        this.device.playlist = this.playlist(); 

        app.showStandby();

        if (this.editMode) {
            provider.updateDevice(this.device.mac_address, this.device, function(data) {
                app.hideStandby();
                self.modal.hide();
                app.signals.deviceSaved.dispatch();
                app.showSuccessToast('Device saved.');
            }, function(error) {
                app.hideStandby();
                app.showErrorToast(error.responseText);
                console.log(error);
            });
        } else {
            provider.addDevice(this.device.mac_address, this.device, function(data) {
                app.hideStandby();
                self.modal.hide();
                app.signals.deviceSaved.dispatch();
                app.showSuccessToast('Device created.');
            }, function(error) {
                app.hideStandby();
                app.showErrorToast(error.responseText);
                console.log(error);
            });
        }
    };

    return Module;
});
