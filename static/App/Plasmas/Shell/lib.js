Ink.createModule('App.Plasmas.Shell', '1', ['App.Plasmas'], function(app) {
    var Module = function() {
        this.definedRoutes = app.definedRoutes;
        this.modalModule = app.modalModule;
        this.alertModule = app.alertModule;
        this.infoModule = app.infoModule;
        this.appTitle = app.appTitle;
    };

    Module.prototype.afterRender = function() {
        this.menu=new Ink.UI.Toggle('#mainMenuTrigger');
        app.signals.shellRendered.dispatch();
    };
    
    Module.prototype.dismissMenu = function() {
        this.menu._dismiss();  
        return true;
    };

    return new Module();
});
