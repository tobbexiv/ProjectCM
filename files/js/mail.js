/**
 * Mail set of functions.
 */
var mail = new function Calendar() {
	/**
	 * Storage for accessing <code>this</code> as reference to Calendar in subfunctions. Do <b>NOT</b> delete!
	 * 
	 * @type	Calendar
	 */
	var _this = this;
	
	/**
	 * Class for Helper functions for the calendar.
	 */
	var _Helper = function() {
		/**
		 * Duration of the animation of hints.
		 */
		var _animationDuration = 1000;
		
		/**
		 * Delay for hiding a hint.
		 */
		var _messageDelay = 5000;
		
		/**
		 * Shows one (or more) hint(s) to the user.
		 * 
		 * @param	{string|string[]}	hint
		 *   The hint(s) to be shown.
		 * @param	{string}			type
		 *   The type of the hint. Possible are success and error.
		 * @param	{function}			callback
		 *   A callback to be run after hiding. (otpional)
		 */
		this.showHint = function(message, type, callback) {
			var messageBar = $('#message_bar');
			
			if(typeof message == 'string') {
				message = [message];
			}
			
			if(!callback) {
				callback = function() { return false; };
			}
			
			for(var i = 0; i < message.length; i++) {
				var messageWrapper = $('<p />', {'class': 'message ' + type, 'style': 'display: none;'}).appendTo(messageBar).html(message[i]);
				messageWrapper.fadeIn(_animationDuration).delay(_messageDelay).fadeOut(_animationDuration, function() { messageWrapper.remove(); callback(); });
				messageWrapper.click(function() { messageWrapper.stop().fadeOut(_animationDuration, function() { messageWrapper.remove(); callback(); }); });
			}
		};

		this.updateUserName = function(userName) {
			$('#user').text(userName);
		}
		
		/**
		 * Get the data from the api.
		 * 
		 * @param	{string}		urlToCall
		 *   The url to call.
		 * @param	{mixed[]}		requestJSON
		 *   The data to be passed as JSON (not stringified yet).
		 * @param	{function[]}	callback
		 *   Callbacks for success and fail. (optional)
		 *   callback.done: success	(optional)
		 *   callback.fail:	fail	(optional)
		 */
		this.getJsonData = function(urlToCall, requestJSON, callback) {
			if(!callback) {
				callback = {};
			}
			
			if(!callback.success) {
				callback.success = function() { return false; };
			}
			
			if(!callback.fail) {
				callback.fail = function() { return false; };
			}
			
			var callbackSucces = function(data) {
				var parsed = data;

				if(typeof data === "string") {
					parsed = JSON.parse(data);
				}
				
				_this.Helper.updateUserName(parsed.userName);

				if(parsed.success) {
					callback.success(parsed.data);
				} else {
					_this.Helper.showHint(parsed.errors, 'error');
				}
			};
			
			var callbackFail = function() {
				_this.Helper.showHint('The server request failed!', 'error');
				callback.fail();
			};
			
			var jsonData = JSON.stringify(requestJSON);
			jsonData = jsonData.replace(/&/g, '%26');
			
			$.ajaxSetup({
				beforeSend: function(xhr, settings) {
					xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
				}
			});
			
			var request = $.ajax({
				url: 		 urlToCall,
				type: 		 'POST',
				data: 		 jsonData,
				contentType: 'application/json; charset=utf-8',
				dataType: 	 'json',
				cache:		 'false',
				timeout:	 10000
			});
			
			request.done(callbackSucces);
			request.fail(callbackFail);
		};

		var _showForm = function(urlToCall, parent, formData, callbackSuccess) {
			if(/id="login_form"/.test(formData)) {
				location.href = '/';
			}

			parent.html(formData);
			$('#save').click(function() {
				_this.Helper.sendForm(urlToCall, this, parent, callbackSuccess);
			});
		}

		this.getForm = function(urlToCall, parent, callbackSuccess) {
			var callbackSucces = function(data) {
				_showForm(urlToCall, parent, data, callbackSuccess);
			};
			
			var callbackFail = function() {
				_this.Helper.showHint('The server request failed!', 'error');
				callback.fail();
			};
			
			$.ajaxSetup({
				beforeSend: function(xhr, settings) {
					xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
				}
			});
			
			var request = $.ajax({
				url: 		 urlToCall,
				type: 		 'GET',
				cache:		 'false',
				timeout:	 10000
			});
			
			request.done(callbackSucces);
			request.fail(callbackFail);
		};

		this.sendForm = function(urlToCall, submit_button, parentElement, callbackSuccess) {
			var data = $(submit_button).parent('form').serialize();
			
			var callbackSucces = function(data) {
				if(/<form method="post">/.test(data)) {
					_showForm(urlToCall, parentElement, data);
					return false;
				}

				_this.Overlay.hide();
				if(callbackSuccess) {
					callbackSuccess();
				}
				var parsedData = data;

				if(typeof data === "string") {
					parsedData = JSON.parse(data);
				}

				_this.Helper.updateUserName(parsedData.userName);
				_this.Helper.showHint(parsedData.data, parsedData.success == true ? 'success' : 'error');

			};
			
			var callbackFail = function() {
				_this.Helper.showHint('The server request failed!', 'error');
			};
			
			$.ajaxSetup({
				beforeSend: function(xhr, settings) {
					xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
				}
			});
			
			var request = $.post(urlToCall, data);
			
			request.done(callbackSucces);
			request.fail(callbackFail);
		};
		
		/**
		 * Returns the animation duration.
		 * 
		 * @return	{int}
		 *   The animation duration.
		 */
		this.getAnimationDuration = function() {
			return _animationDuration;
		}
	}
	
	/**
	 * Helper funtions for the Calendar.
	 */
	this.Helper = new _Helper;

	var _Message = function() {
		this.showSendForm = function() {
			var title	= 'Send mail';

			var callback = function(parent) {
				_this.Helper.getForm('/mail/message/send/', parent, function() {});
			}
			
			_this.Overlay.show(title, null, callback);
		};
	}

	this.Message = new _Message;
	
	/**
	 * Class for overlay operations.
	 */
	function _Overlay() {
		/**
		 * Prepare the overlay for showing.
		 */
		var _prepareOverlay = function() {
			var overlayWrapper			= $('<div />', {'id': 'overlay_wrapper'}).appendTo(document.body).css('display', 'none');
			var overlayBackground		= $('<div />', {'id': 'overlay_background'}).appendTo(overlayWrapper);
			var overlayPanelContainer	= $('<div />', {'id': 'overlay_panel_container'}).appendTo(overlayWrapper);
			var overlayPanelHeader		= $('<div />', {'id': 'overlay_panel_header'}).appendTo(overlayPanelContainer);
			var overlayPanelCloseButton	= $('<span />', {'id': 'overlay_panel_close'}).appendTo(overlayPanelHeader).html('&times;');
			var overlayPanelTitle		= $('<span>', {'id': 'overlay_panel_title'}).appendTo(overlayPanelHeader);
			var overlayPanelContent		= $('<div />', {'id': 'overlay_panel_content'}).appendTo(overlayPanelContainer);
			
			var hide = function() {
				overlayWrapper.fadeOut(_this.Helper.getAnimationDuration(), function() {
					overlayPanelTitle.empty();
					overlayPanelContent.empty();
				});
			}
			
			overlayBackground.click(hide);
			overlayPanelCloseButton.click(hide);
		};
		
		/**
		 * Show a overlay.
		 * 
		 * @param	{string}	title
		 *   The title of the overlay.
		 * @param	{mixed}		content
		 *   The content of the overlay. e.g. jQuery, jQuery[], text, html
		 * @param	{function}	callback
		 *   A callback to be called after appending the content.
		 */
		this.show = function(title, content, callback) {
			if($('#overlay_wrapper').length == 0) {
				_prepareOverlay();
			}
			
			$('#overlay_panel_title').empty().text(title);
			$('#overlay_panel_content').empty();

			if(content) {
				$('#overlay_panel_content').append(content);
			}
			
			if(callback) {
				callback($('#overlay_panel_content'));
			}
			
			$('#overlay_wrapper').fadeIn(_this.Helper.getAnimationDuration());
		};

		/**
		 * Hide the overlay.
		 */
		this.hide = function() {
			$('#overlay_panel_close').click();
		};
	}
	
	/**
	 * Overlay functions.
	 */
	this.Overlay = new _Overlay();
}