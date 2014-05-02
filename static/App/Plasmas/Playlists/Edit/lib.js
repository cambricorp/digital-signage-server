Ink.createModule('App.Plasmas.Playlists.Edit', '1', ['App.Plasmas', 'App.Plasmas.DataProvider', 'Ink.Data.Binding_1', 'Ink.UI.Aux_1'], function(app, provider, ko, inkAux) {
    var Module = function(modal) {
        var self = this;

        this.modal = modal;
        this.params = modal.params;
        
        this.editMode = !!this.params.playlist;
        
        this.playlist = (this.params.playlist?inkAux.clone(this.params.playlist):undefined);

        this.name = ko.observable(this.playlist?this.playlist.name:'').extend({
            required: true,
            minLength: 3,
            maxLength: 15,
            pattern: {
                 message: 'Only alfanumeric characters and hifen, please',
                 params: '^[a-zA-Z0-9\-]*$'
            }
        }); 

        this.description = ko.observable(this.playlist?this.playlist.description:'');

        modal.confirmHandler = this.savePlaylist.bind(this);

        modal.confirmDisabled(ko.computed(function() {
            return (!self.name.isValid());
        }));
    };

    Module.prototype.savePlaylist = function() {
        var self = this;

        if (!this.playlist) {
            this.playlist = {
                assets: []
            };
        }

        this.playlist.name = this.name();
        this.playlist.description = this.description();

        app.showStandby();

        if (this.editMode) {
            provider.updatePlaylist(this.playlist.name, this.playlist, function(data) {
                app.hideStandby();
                self.modal.hide();
                app.signals.playlistSaved.dispatch();
                app.showSuccessToast('Playlist saved.');
            }, function(error) {
                app.hideStandby();
                app.showErrorToast(error.responseText);
                console.log(error);
            });
        } else {
            provider.addPlaylist(this.playlist.name, this.playlist, function(data) {
                app.hideStandby();
                self.modal.hide();
                app.signals.playlistSaved.dispatch();
                app.showSuccessToast('Playlist created.');
            }, function(error) {
                app.hideStandby();
                app.showErrorToast(error.responseText);
                console.log(error);
            });
        }
    };

    return Module;
});
