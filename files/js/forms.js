/**
 * 
 */
var _UI_Plus = function() {
	var _self = this;
	
	/**
	 * Instantiate a new set of localisation functions.
	 * 
	 * @inner
	 * 
	 * @class
	 * @classdesc	Functions for localisating the script.
	 */
	function _Language() {
		/*--------------------------------------------*
		 * Private variables, functions and settings. *
		 *--------------------------------------------*/
		
		/**
		 * Default language code - default for this server.
		 * 
		 * @private
		 * @inner
		 * 
		 * @type	string
		 */
		var _languageCode = typeof LanguageData != 'undefined' && typeof LanguageData.defaultCode != 'undefined' ? LanguageData.defaultCode : 'en';
		
		/**
		 * The name of the language.
		 * 
		 * @private
		 * @inner
		 * 
		 * @type	string
		 */
		var _languageName = typeof LanguageData != 'undefined' && typeof LanguageData[_languageCode] != 'undefined' && typeof LanguageData[_languageCode].name != 'undefined' ? LanguageData[_languageCode].name : 'English';
		
		/**
		 * The texts of the used language.
		 * 
		 * @private
		 * @inner
		 * 
		 * @type	string
		 */
		var _languageText = typeof LanguageData != 'undefined' && typeof LanguageData[_languageCode] != 'undefined' && typeof LanguageData[_languageCode].text != 'undefined' ? LanguageData[_languageCode].text : {};
		
		/*-------------------------------------------*
		 * Public variables, functions and settings. *
		 *-------------------------------------------*/
		/**
		 * Return the name of the used language.
		 * 
		 * @instance
		 * 
		 * @return	{string}
		 *   The language name.
		 */
		this.getLanguageName = function(languageCode) {
			return LanguageData && LanguageData[_languageCode] && LanguageData[_languageCode].name ? LanguageData[_languageCode].name : '';
		};
		
		/**
		 * Set the language code which is used.
		 * 
		 * @instance
		 * 
		 * @param	{string}	code
		 * 	 The language code.
		 */
		this.setLanguage = function(languageCode) {
			_languageCode	= languageCode;
			_languageName	= this.getLanguageName(languageCode);
			_usedText		= typeof LanguageData != 'undefined' && typeof LanguageData[_languageCode] != 'undefined' && typeof LanguageData[_languageCode].text != 'undefined' ? LanguageData[_languageCode].text : {};
		};
		
		/**
		 * Return a string which is defined by its placeholder. If the string contains variables defined with %$nr,
		 * they are replaced with the content of the array at this index.
		 * 
		 * @instance
		 * 
		 * @param	{string}	name
		 *   The name of the placeholder.
		 * @param	{mixed[]}	vars
		 *   An array containing variables for replacing in the language string. (optional)
		 *
		 * @return	{string}
		 *   The text.
		 */
		this.getText = function(name, vars) {
			var erg = name;
	
			var parts = name.split('_');
	
			if(parts) {
				var txt = _languageText ? _languageText[parts[0]] : null;
	
				for(var i = 1; i < parts.length; i++) {
					if(txt && typeof txt[parts[i]] != 'undefined') {
						txt = txt[parts[i]];
					} else {
						txt = erg;
						break;
					}
				}
	
				// If the text type is not an object, a function or undefined.
				if(typeof txt != 'object' && typeof txt != 'function' && typeof txt != 'undefined') {
					erg = txt + '';
				}
				
				if(vars) {
					for(var i = 0; i < vars.length; i++) {
						var regex = new RegExp('%\\$' + (i + 1), 'g');
						erg = erg.replace(regex, vars[i] + '');
					}
				}
			}
			
			if(erg == name) {
				console.log('Language.getText: No translation available for "' + name + '" in language ' + _languageName + ' (' + _languageCode + ')');
			}
			
			// Return the text.
			return erg;
		};
		
		/**
		 * Synonymous function for {@link UI_Plus~Language#getText}.<br>
		 * Return a string which is defined by its placeholder. If the string contains variables defined with %$nr,
		 * they are replaced with the content of the array at this index.
		 * 
		 * @instance
		 * 
		 * @param	{string}	name
		 *   The name of the placeholder.
		 * @param	{mixed[]}	vars
		 *   An array containing variables for replacing in the language string. (optional)
		 *
		 * @return	{string}
		 *   The text.
		 */
		this.$ = function(name, vars) {
			return this.getText(name, vars);
		};
	}
	
	/**
	 * Functions for localisation of the script.
	 * 
	 * @instance
	 * 
	 * @type	IkariamCore~Language
	 */
	this.Language = new _Language;
	
	var _Replacer = function() {
		this.checkboxes = function() {
			var cbs = $('input[type="checkbox"]:not(.replaced)');
			
			var _checkProps = function(checkbox, replacement) {
				var cb = $(checkbox);
				var rep = $(replacement);
				
				if(cb.prop('checked')) {
					rep.addClass('checked');
				} else {
					rep.removeClass('checked');
				}
				
				if(cb.prop('disabled')) {
					rep.addClass('disabled');
				} else {
					rep.removeClass('disabled');
				}
			};
			
			$(cbs).each(function() {
				var wrapper = $('<div/>', {'class': 'checkboxWrapper wrapper'});
				var checkbox = $(this);
				checkbox.wrap(wrapper);
				
				var replacement = $('<span/>', {'class': 'checkbox'}).appendTo($(this).parent());
				replacement.text(checkbox.attr('title'));
				
				_checkProps(checkbox, replacement);
				
				checkbox.on('update', function(){ _checkProps(checkbox, replacement); });
				replacement.on('click', function() { checkbox.click(); checkbox.trigger('update'); });
				
				checkbox.addClass('replaced');
			});
		};
		
		this.radioButtons = function() {
			
		};
		
		this.selectFields = function() {
			
		};
		
		this.fileUploader = function() {
			var uploaders = $('input[type="file"]:not(.replaced)');
			
			var _checkProps = function(fileUploader, replacement) {
				var uploader = $(fileUploader);
				var rep = $(replacement);
				
				if(uploader.prop('disabled')) {
					rep.addClass('disabled');
				} else {
					rep.removeClass('disabled');
				}
			};
			
			var _setText = function(span, fileUploader) {
				var selected = fileUploader.val();
				selected = selected.length > 0 ? selected : _self.Language.$('fileUploader_noFileSelected');
				span.text(selected);
			};
			
			$(uploaders).each(function() {
				var wrapper = $('<div/>', {'class': 'fileUploaderWrapper wrapper'});
				var uploader = $(this);
				uploader.wrap(wrapper);
				
				var replacementButton = $('<input/>', {'type': 'button', 'class': 'fileUploader'}).appendTo($(this).parent());
				var replacementSpan = $('<span/>', {'class': 'fileUploader'}).appendTo($(this).parent());
				
				replacementButton.val(_self.Language.$('fileUploader_search'));
				
				_checkProps(uploader, replacementButton);
				_setText(replacementSpan, uploader);
				
				uploader.on('update change', function(){ setTimeout(function() { _setText(replacementSpan, uploader); }, 0); });
				replacementButton.on('click', function() { uploader.click(); _checkProps(uploader, this); });
				
				uploader.addClass('replaced');
			});
		};
		
		this.checkResetButtons = function() {
			var _confirmFunction = function() {
				if(!confirm(_self.Language.$('resetButton_confirmationMessage'))) {
					return false;
				}
				
				setTimeout(function() { $('input').trigger('update'); }, 0);
			}
			
			$('input[type="reset"]:not(.handlerSet)').addClass('handlerSet').on('click', _confirmFunction);
		};

		this.checkCancelButtons = function() {
			var _confirmFunction = function() {
				if(!confirm(_self.Language.$('cancelButton_confirmationMessage'))) {
					return false;
				}
			}
			
			$('form a.cancel:not(.handlerSet)').addClass('handlerSet').on('click', _confirmFunction);
		};
		
		this.checkAll = function(){
			// this.checkboxes();
			this.radioButtons();
			this.selectFields();
			this.fileUploader();
			
			this.checkResetButtons();
			this.checkCancelButtons();
		};
	};
	
	this.Replacer = new _Replacer;
};

var UI_Plus = new _UI_Plus();

$(document).ready(function() {
	UI_Plus.Replacer.checkAll();
});