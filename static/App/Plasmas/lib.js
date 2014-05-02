/**
 * @module App.Plasmas
 * @desc This is the application main app module (inherits from Ink.App)
 * @version 1
 */    

Ink.createModule('App.Plasmas', '1', ['Ink.App_1', 'App.Plasmas.DataProvider', 'Ink.Data.Binding_1', 'Ink.Plugin.Signals_1', 'Ink.Data.Grid_1', 'Ink.Data.AutoComplete_1', 'Ink.Data.Validation_1'], function(App, provider, ko, Signal) {
    
    // App constructor (only data initialization logic)
    var Module = function() {
        App.call(this, 'playlists', 'playlists'); // Call the base initialization logic (set default route, undefined route)

        this.appTitle = 'Digital signage administration';

        provider.init(this.signals);
        
        // Knockout validation plugin setup
        ko.validation.init({insertMessages: false, messagesOnModified: false});
    };
    
    Module.prototype = new App();
    Module.constructor = Module;

    /*
     * Define routing maps
     * 
     */
    Module.prototype.listVisibleRoutes = function() {
        return [
          {isActive: ko.observable(true), caption: 'Playlists', hash: 'playlists', module: 'App.Plasmas.Playlists', arguments: {}},
          {isActive: ko.observable(false), caption: 'Devices', hash: 'devices', module: 'App.Plasmas.Devices', arguments: {}},
        ];
    };

    Module.prototype.listInvisibleRoutes = function() {
        return [
          /*
          {hash: 'new', module: 'App.Tasks.EditTask'},
          {hash: 'edit\\?id=:id', module: 'App.Tasks.EditTask'}
          */
        ];
    };
    

    /*
     * UI signals setup
     * 
     */
    Module.prototype.addCustomSignals = function() {
        this.signals.noSession = new Signal();  
        this.signals.playlistSaved = new Signal();
        this.signals.assetSaved = new Signal();
        this.signals.deviceSaved = new Signal();

        this.signals.noSession.add(this.noSession, this);
    };

    Module.prototype.noSession = function() {
        document.location = 'auth/login';
    }
    
    /*
     * Application startup logic
     * 
     */
    Module.prototype.ready = function() {
        /// Do your custom initialization stuff here, and then call start();
        this.start();
    };
    
    return new Module();
});
