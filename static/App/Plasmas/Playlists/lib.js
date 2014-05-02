Ink.createModule('App.Plasmas.Playlists', '1', ['App.Plasmas', 'Ink.Data.Binding_1', 'App.Plasmas.DataProvider', 'Ink.UI.Aux_1'], function(app, ko, provider, inkAux) {
    var Module = function() {
        var self=this;
        
        this.assetMap = {};
        
        this.showKanban = ko.observable(true);
        
        this.kanbanMode = ko.observable(true);
        
        this.masonMode = ko.computed(function() {
           return !self.kanbanMode(); 
        });
        
        this.assets = ko.observableArray();
        
        this.playlists = ko.observableArray();
        
        this.assets = ko.observableArray();

        this.assetTypeFilter = ko.observable('All');
        
        this.assetSearchFilter = ko.observable('');
        
        this.filteredAssets = ko.computed(function() {
            var results = [];
            var assets = self.assets();
            var asset;
            var i;
            var typeFilter = self.assetTypeFilter();
            var searchFilter = self.assetSearchFilter().toLowerCase();
            
            for (i=0; i<assets.length; i++) {
                asset = assets[i];
                
                if ( ( (typeFilter == 'All') || (typeFilter==asset.assetData.type) ) &&
                     ( (searchFilter.length==0) || (asset.assetData.description.toLowerCase().indexOf(searchFilter)>=0) || (asset.assetData.uri.toLowerCase().indexOf(searchFilter)>=0) ) ) {
                    results.push(asset);
                }
            }            
            
            return results;
        });
        
        this.sections = ko.computed(function() {
            return [{
                        offset: self.sectionScrollOffset.bind(self, 'Assets'),
                        title: 'Assets', 
                        headerTemplate: 'assetsSectionHeaderTemplate', 
                        footerTemplate: 'assetsSectionFooterTemplate', 
                        items: self.filteredAssets, 
                        droppable: false,
                        assetTypeFilter: self.assetTypeFilter,
                        assetSearchFilter: self.assetSearchFilter,
                        newAssetHandler: self.newAssetHandler.bind(this)
                   }].
                   concat(self.playlists());
        });
        
        this.hideUnpinnedPlaylists=ko.observable(false);
        
        app.signals.playlistSaved.add(this.loadPlaylists.bind(this));
        app.signals.assetSaved.add(this.loadAssets.bind(this));
    };

    Module.prototype.initialize = function(data) {
        this.loadAssets();
    };

    Module.prototype.getContentTemplate = function(type) {
        switch (type) {
            case 'video':
            case 'web':
                return 'uriAssetCardTemplate';
            case 'meokanal':
                return 'kanalAssetCardTemplate';
            case 'playlist':
                return 'playlistAssetCardTemplate';
        }
        
        throw 'getContentTemplate:Invalid content type';
    };
    
    Module.prototype.getContent = function(asset) {
        var content = inkAux.clone(asset);
        
        switch (content.type) {
            case 'meokanal':
                content.kanal = content.uri.split('kanal://')[1]; 
                break;
            case 'playlist':
                content.playlist = content.uri.split('playlist://')[1]; 
                break;
        }
        
        return content;
    };

    Module.prototype.getCardForAsset = function(asset, playlistTag) {
        return {
            id: asset.guid,
            title: asset.description,
            contentTemplate: this.getContentTemplate(asset.type),
            content: this.getContent(asset),
            assetData: asset,
            cardClass: 'asset-card-'+asset.type,
            moveOnDrop: false,
            editIcon: 'icon-cog',
            editHandler: this.editAssetHandler.bind(this, asset),
            playlistTag: playlistTag
        };
    };
    
    Module.prototype.loadAssets = function() {
        var self=this;
        
        provider.listAssets(function(data) {
            var assetsJSON = data.responseJSON.assets;
            var i;
            var assets = [];
            var asset;

            self.assetMap = {};
            
            for (i=0; i<assetsJSON.length; i++) {
                asset = assetsJSON[i];
                assets.push(self.getCardForAsset(asset));
                self.assetMap[asset.guid] = asset;
            }
            
            self.assets(assets);
            
            self.loadPlaylists();
        });
    };
    
    Module.prototype.loadPlaylists = function() {
        var self=this;
        
        provider.listPlaylists(function(data) {
            var playlistsJSON = data.responseJSON.playlists;
            var i, assetIndex;
            var lists = [];
            var list;
            var assets;
            var asset;
            var taggedList;
            
            for (i=0; i<playlistsJSON.length; i++) {
                list = playlistsJSON[i];
                assets = [];
                
                taggedList = self.taggedObservable(ko.observableArray(), list);
                
                for (assetIndex=0; assetIndex<list.assets.length; assetIndex++) {
                    asset = self.assetMap[list.assets[assetIndex].guid];
                    if (asset) {
                        assets.push(self.cloneItem(self.getCardForAsset(asset, taggedList), taggedList));
                    }
                }
                
                taggedList(assets);
                
                lists.push({
                    headerTemplate: 'playlistSectionHeaderTemplate',
                    offset: self.sectionScrollOffset.bind(self, list.name),
                    title: list.name,
                    settingsHandler: self.playListSettingsHandler.bind(self, list),
                    items: taggedList,
                    pinned: ko.observable(false),
                    css: ko.observable('unpinned'),
                    playlistPinToggleHandler: self.playlistPinToggleHandler.bind(self),
                });
            }
            
            self.playlists(lists);

        });
    };
    
    Module.prototype.afterRender = function() {
    };
    
    Module.prototype.playListSettingsHandler = function(playlist) {
        app.showSmallModalWindow('Edit playlist', 'App.Plasmas.Playlists.Edit', {playlist: playlist, taskButtons: [{caption: 'Remove', handler: this.removePlaylistHandler.bind(this, playlist), icon: 'icon-trash', cssClass: ''}]});
    };

    Module.prototype.removePlaylistHandler = function(playlist, modal) {
        var self = this;
        
        app.showStandby();
        
        provider.deletePlaylist(playlist.name, function(data) {
            self.loadPlaylists();
            app.hideStandby();
            modal.hide();
        }, function(error) {
            app.hideStandby();
            modal.hide();
            app.showErrorToast(error.responseText);
            console.log(error);
        });
    };
    
    Module.prototype.editAssetHandler = function(asset) {
        app.showSmallModalWindow('Edit asset', 'App.Plasmas.Assets.Edit', {asset: asset, taskButtons: [{caption: 'Remove', handler: this.removeAssetHandler.bind(this, asset), icon: 'icon-trash', cssClass: ''}]});
    };

    Module.prototype.removeAssetHandler = function(asset, modal) {
        var self = this;
        
        app.showStandby();
        
        provider.deleteAsset(asset.guid, function(data) {
            self.loadAssets();
            app.hideStandby();
            modal.hide();
        }, function(error) {
            app.hideStandby();
            modal.hide();
            app.showErrorToast(error.responseText);
            console.log(error);
        });
    };
    
    Module.prototype.previewMoveHandler = function(listItemsObservable, assetsArray, listIndex) {
        var assetIndex;
        
        for (assetIndex = 0; assetIndex < assetsArray.length; assetIndex++) {
            assetsArray[assetIndex]=this.cloneItem(assetsArray[assetIndex], listItemsObservable);
        }
        
        return true;
    };

    Module.prototype.cardsMovedHandler = function(listItemsObservable, assetsArray, listIndex) {
        var playlist = inkAux.clone(listItemsObservable.tag);
        var assets = [];
        var cards = listItemsObservable();
        var i;
        
        for (i = 0; i < cards.length; i++) {
            assets.push({guid: cards[i].id})
        }
        playlist.assets = assets;
        
        this.savePlaylistSilently(playlist);
    };

    Module.prototype.savePlaylistSilently = function(playlist) {
        this.savePlaylist(playlist, true);
    };
    
    Module.prototype.savePlaylist = function(playlist, silent) {
        var self = this;
        
        app.showStandby();

        provider.updatePlaylist(playlist.name, playlist, function(data) {
            if ( (typeof silent == 'undefined') || !silent) {
                self.loadPlaylists();
            }
            app.hideStandby();
        }, function(error) {
            app.hideStandby();
            app.showErrorToast(error.responseText);
            console.log(error);
        });
    };
    
    Module.prototype.cloneItem = function(item, targetPlaylist) {
        clone=inkAux.clone(item);
        clone.editIcon='icon-trash';
        clone.editHandler = this.removeItem.bind(this, clone, targetPlaylist);
        
        if (item.playlistTag) {
            item.moveOnDrop = (item.playlistTag.name==targetPlaylist.tag.name);
        }

        clone.playlistTag = targetPlaylist.tag;
        
        return clone;
    };
    
    Module.prototype.removeItem = function(item, pAssetsObservable) {
        var playlist = pAssetsObservable.tag;
        var pl = inkAux.clone(pAssetsObservable.tag);
        var i;

        pAssetsObservable.remove(item);
        pl.assets = [];
        
        for (i=0; i<pAssetsObservable().length; i++) {
            pl.assets.push(pAssetsObservable()[i].assetData);
        }
        
        this.savePlaylistSilently(pl);
    };
    
    Module.prototype.taggedObservable = function(observable, tag) {
        observable.tag = tag;
        
        return observable;
    }
    
    Module.prototype.sectionScrollOffset = function(section, card) {
        var scrollTop=0;
        var parentNode = card.parentNode;

        while ((typeof parentNode.scrollTop=='number') && (scrollTop==0)) {
            scrollTop+=parentNode.scrollTop;
            parentNode = parentNode.parentNode;
        }
        
        return {left: 0, top: scrollTop};
    };

    Module.prototype.newAssetHandler = function() {
        app.showSmallModalWindow('New asset', 'App.Plasmas.Assets.Edit', {});
    };
    
    Module.prototype.newPlaylistHandler = function() {
        app.showSmallModalWindow('New playlist', 'App.Plasmas.Playlists.Edit', {});
    };

    Module.prototype.playlistPinToggleHandler = function(playlist) {
        playlist.pinned(!playlist.pinned());
        playlist.css(!playlist.pinned()?'unpinned':'');
    };

    Module.prototype.toggleHideUnpinnedHandler = function() {
        this.hideUnpinnedPlaylists(!this.hideUnpinnedPlaylists());
    };
    
    Module.prototype.afterKanbanRender = function(sectionEls, kanban) {
        if (this.masonMode()) {
            var container = document.getElementById('playlistsKanbanViewport');
            var msnry = new Masonry(container, {
                itemSelector: '.section'
            });
            
            window.setTimeout(function() {
                msnry.layout();
            }, 500);
        }
    };
    
    Module.prototype.toggleMode = function() {
        this.kanbanMode(!this.kanbanMode());

        this.showKanban(false);
        this.showKanban(true);
    };
    
    return new Module();
});
