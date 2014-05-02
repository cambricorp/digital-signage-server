Ink.createModule('App.Plasmas.Assets.Edit', '1', ['App.Plasmas', 'App.Plasmas.DataProvider', 'Ink.Data.Binding_1', 'Ink.UI.Aux_1'], function(app, provider, ko, inkAux) {
    function genGuid() {
        function S4() {
            return (((1+Math.random())*0x10000)|0).toString(16).substring(1); 
        }
        return (S4() + S4() + "-" + S4() + "-4" + S4().substr(0,3) + "-" + S4() + "-" + S4() + S4() + S4()).toLowerCase();    
    }

    var Module = function(modal) {
        var self = this;
        var uriRegex = /(http|ftp|https):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/;

        this.modal = modal;
        this.params = modal.params;
        this.asset = (this.params.asset?inkAux.clone(this.params.asset):undefined);

        this.playlists = ko.observableArray();

        this.assetTypes = ['video', 'web', 'meokanal', 'playlist'];
        
        this.editMode = this.asset==true;

        this.description = ko.observable(this.asset?this.asset.description:'').extend({
            required: true,
            minLength: 3,
            maxLength: 50
        }); 
        
        this.type = ko.observable(this.asset?this.asset.type:'video');

        this.assetTemplateName = ko.computed(function() {
           return self.type()+'AssetTemplate'; 
        });
        
        this.videoUri = ko.observable(this.asset?this.asset.uri:'').extend({
            required: true,
            pattern: {
                message: 'Only valid uris, please',
                params: uriRegex
           }
        });

        this.webUri = ko.observable(this.asset?this.asset.uri:'').extend({
            required: true,
            pattern: {
                message: 'Only valid uris, please',
                params: uriRegex
           }
        });
        
        this.durationSecs = ko.observable(this.asset?this.asset.duration_secs:10).extend({
           required: true,
           min: 1,
           max: 1800, 
        });
        
        this.kanalChannel = ko.observable(this.asset?(this.asset.type=='meokanal'?this.asset.uri.split('kanal://')[1]:''):'').extend({
           required: true,
           digit: true,
           minLength: 1,
           maxLength: 20
        });
        
        this.pin = ko.observable(this.asset?this.asset.pin:undefined).extend({
           required: true,
           digit: true,
           minLength: 4,
           maxLength: 4
        });
        
        this.howMany = ko.observable(this.asset?this.asset.how_many:1).extend({
            required: true,
            number: true,
            min: 0,
            max: 9999
        });
        
        this.playlist = ko.observable(this.asset?(this.asset.type=='playlist'?this.asset.uri.split('playlist://')[1]:''):'').extend({
            required: true,
            minLength: 3,
            maxLength: 15,
            pattern: {
                 message: 'Only alfanumeric characters and hifen, please',
                 params: '^[a-zA-Z0-9\-]*$'
            }
        });
        
        this.shuffle = ko.observable(this.asset?this.asset.shuffle:true);

        modal.confirmHandler = this.saveAsset.bind(this);

        modal.confirmDisabled(ko.computed(function() {
            return false;
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
    
    Module.prototype.saveAsset = function() {
        var self = this;
        var asset;

        if (!this.asset) {
            asset = {
                    guid: genGuid()
            };
        } else {
            asset = inkAux.clone(this.asset);
        }

        asset.description = this.description();
        asset.type = this.type();
        
        switch (asset.type) {
        case 'video':
            asset.uri = this.videoUri();
            asset.duration_secs = this.durationSecs();
            break;
            
        case 'web':
            asset.uri = this.webUri();
            asset.duration_secs = this.durationSecs();
            break;
            
        case 'meokanal':
            asset.uri = 'kanal://' + this.kanalChannel();
            asset.duration_secs = this.durationSecs();
            asset.pin = this.pin();
            asset.how_many = this.howMany();
            asset.shuffle = this.shuffle();
            break;
            
        case 'playlist':
            asset.uri = 'playlist://' + this.playlist();
            asset.how_many = this.howMany();
            asset.shuffle = this.shuffle();
            break;
        }

        app.showStandby();

        provider.addAsset(asset.guid, asset, function(data) {
            app.hideStandby();
            self.modal.hide();
            app.signals.assetSaved.dispatch();
            app.showSuccessToast('Asset saved.');
        }, function(error) {
            app.hideStandby();
            app.showErrorToast(error.responseText);
            console.log(error);
        });
    };

    return Module;
});
