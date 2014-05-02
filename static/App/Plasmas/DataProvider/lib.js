Ink.createModule('App.Plasmas.DataProvider', '1', ['App.Plasmas.DataProvider.Base'], function(BaseProvider) {
    var Module = function() {
        BaseProvider.call(this);  // Call super constructor
    };

    Module.prototype = new BaseProvider();
    Module.constructor = Module;

    /*
     * Devices
     */
    Module.prototype.listDevices = Module.prototype._buildApiMethod({method: 'GET', uriPath: 'device/list'});

    Module.prototype.addDevice = Module.prototype._buildApiMethod({method: 'POST', uriPath: 'device/detail', hasResourceId: true, hasPostBody: true});

    Module.prototype.updateDevice = Module.prototype._buildApiMethod({method: 'PUT', uriPath: 'device/detail', hasResourceId: true, hasPostBody: true});
    
    Module.prototype.deleteDevice = Module.prototype._buildApiMethod({method: 'DELETE', uriPath: 'device/detail', hasResourceId: true});
    
    /*
     * Assets
     */
    Module.prototype.listAssets = Module.prototype._buildApiMethod({method: 'GET', uriPath: 'asset/list'});

    Module.prototype.addAsset = Module.prototype._buildApiMethod({method: 'POST', uriPath: 'asset/detail', hasResourceId: true, hasPostBody: true});

    Module.prototype.deleteAsset = Module.prototype._buildApiMethod({method: 'DELETE', uriPath: 'asset/detail', hasResourceId: true});

    /*
     * Playlists
     */
    Module.prototype.listPlaylists = Module.prototype._buildApiMethod({method: 'GET', uriPath: 'playlist/list'});

    Module.prototype.addPlaylist = Module.prototype._buildApiMethod({method: 'POST', uriPath: 'playlist/detail', hasResourceId: true, hasPostBody: true});

    Module.prototype.updatePlaylist = Module.prototype._buildApiMethod({method: 'PUT', uriPath: 'playlist/detail', hasResourceId: true, hasPostBody: true});
    
    Module.prototype.deletePlaylist = Module.prototype._buildApiMethod({method: 'DELETE', uriPath: 'playlist/detail', hasResourceId: true});

    
    /*
     * Statistics
     */
    Module.prototype.listStats = Module.prototype._buildApiMethod({method: 'GET', uriPath: 'stats/list', hasResourceId: true});
    
    /*
     * Alerts
     */
    Module.prototype.sendAlerts = Module.prototype._buildApiMethod({method: 'POST', uriPath: 'alerts/batch', hasPostBody: true});

    Module.prototype.listTemplates = Module.prototype._buildApiMethod({method: 'GET', uriPath: 'alerts/templates'});
    

    return new Module();
});
