Ink.createModule('App.Plasmas.Devices.Alert', '1', ['App.Plasmas', 'App.Plasmas.DataProvider', 'Ink.Data.Binding_1'], function(app, provider, ko) {
    var Module = function(modal) {
        var self = this;
        var uriRegex = /(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/;

        this.modal = modal;
        this.params = modal.params;
        this.devices = this.params.devices;
        this.template = ko.observable();
        this.availableTemplates = ko.observableArray();
        this.duration = ko.observable(30);
        
        modal.confirmHandler = this.sendAlertHandler.bind(this);

        modal.confirmDisabled(ko.computed(function() {
            return typeof self.template() == 'undefined';
        }));
        
        this.loadTemplates();
    };
    
    Module.prototype.loadTemplates = function() {
        var self=this;
        
        provider.listTemplates(function(data) {
            var templates = data.responseJSON.templates;
            
            self.availableTemplates(templates);
        });
    };
    
    Module.prototype.sendAlertHandler = function() {
        var self=this;
        var uri;
        var template=this.template();
        var duration=this.duration();
        var i;
        var param;
        var batch;

        uri='' + duration + ',' + template.uri;
        for (i=0; i<template.params.length; i++) {
            param = template.params[i].value;
            if (param && param.trim().length > 0) {
                uri+='#'+param;
            }
        }
        
        batch = {
                mac_address_list: [],
                uri: uri
        };
        
        for (i=0; i<this.devices.length; i++) {
            batch.mac_address_list.push(this.devices[i].mac_address);
        }
        
        app.showStandby();

        provider.sendAlerts(batch, function(data) {
            app.hideStandby();
            self.modal.hide();
            app.showSuccessToast('Alert sent to devices.');
        }, function(error) {
            app.hideStandby();
            app.showErrorToast(error.responseText);
            console.log(error);
        });
    };

    return Module;
});
