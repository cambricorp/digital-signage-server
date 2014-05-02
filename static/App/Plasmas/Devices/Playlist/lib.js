Ink.createModule('App.Plasmas.Devices.Playlist', '1', ['App.Plasmas', 'App.Plasmas.DataProvider', 'Ink.Data.Binding_1'], function(app, provider, ko) {
    var Module = function(modal) {
        var self = this;

        this.modal = modal;
        this.params = modal.params;
        this.device = this.params.device;
    };

    return Module;
});
