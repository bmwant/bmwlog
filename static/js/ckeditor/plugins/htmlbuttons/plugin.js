/**
 * Modified CKEditor plugin to add one button to my editor
 */

CKEDITOR.plugins.add( 'htmlbuttons', {
	requires: ['menubutton'],
	init : function( editor )
	{
		var buttonsConfig = editor.config.htmlbuttons,
			plugin = this;
		if (!buttonsConfig)
			return;

		function createCommand( definition )
		{
			return {
				exec : function( editor ) {
                    var selected_text = editor.getSelection().getSelectedText(); // Get Text
                    var newElement = new CKEDITOR.dom.element(definition.html); // Make element by tag name
                    //newElement.setAttributes({style: 'myclass'})                 // Set Attributes
                    newElement.setText(selected_text);                           // Set text to element
                    editor.insertElement(newElement);                            // Add Element
                }
			};
		}

		function createMenuButton( definition )
		{
			var itemsConfig = definition.items;
			var items = {};

			// add menuitem from config.itemlist
			for (var i = 0; i < itemsConfig.length; i++ ) {
				var item = itemsConfig[ i ];
				var commandName = item.name;
				editor.addCommand( commandName, createCommand( item ) );

				items[ commandName ] = {
					label: item.title,
					command : commandName,
					group: definition.name,
					role: 'menuitem'
				};

			}
			editor.addMenuGroup( definition.name, 1 );
			editor.addMenuItems( items );

			return {
				label: definition.title,
				icon: plugin.path + definition.icon,
				toolbar: definition.toolbar || 'insert',
				onMenu: function() {
					var activeItems = {};

					for ( var item in items )
						activeItems[ item ] = CKEDITOR.TRISTATE_OFF;

					return activeItems;
				}
			};
		}

		// Create the command for each button
		for(var i=0; i<buttonsConfig.length; i++)
		{
			var definition = buttonsConfig[ i ];
			var commandName = definition.name;
			console.log(definition.html);
			if (definition.html)
			{
				editor.addCommand( commandName, createCommand( definition ) );

				editor.ui.addButton( commandName,
				{
					label : definition.title,
					command : commandName,
					icon : plugin.path + definition.icon
				});
			}
			else
			{
				// create a menubutton
				var menuButton = createMenuButton( definition );

				// insert menubutton to toolbar
				editor.ui.add( commandName,  CKEDITOR.UI_MENUBUTTON, menuButton);
			}
		}
	} //Init

} );
