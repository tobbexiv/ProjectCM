/**
 * Calendar set of functions.
 */
var cal = new function Calendar() {
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
		 * Storage for calendar settings for the datetimepicker.
		 */
		var _withSpinners = {
			create: function(tp_inst, obj, unit, val, min, max, step){
				$('<input class="ui-timepicker-input" value="'+val+'" style="width:50%">')
					.appendTo(obj)
					.spinner({
						min: min,
						max: max,
						step: step,
						change: function(e,ui){ // key events
								// don't call if api was used and not key press
								if(e.originalEvent !== undefined)
									tp_inst._onTimeChange();
								tp_inst._onSelectHandler();
							},
						spin: function(e,ui){ // spin events
								tp_inst.control.value(tp_inst, obj, unit, ui.value);
								tp_inst._onTimeChange();
								tp_inst._onSelectHandler();
							}
					});
				return obj;
			},
			options: function(tp_inst, obj, unit, opts, val){
				if(typeof(opts) == 'string' && val !== undefined)
						return obj.find('.ui-timepicker-input').spinner(opts, val);
				return obj.find('.ui-timepicker-input').spinner(opts);
			},
			value: function(tp_inst, obj, unit, val){
				if(val !== undefined)
					return obj.find('.ui-timepicker-input').spinner('value', val);
				return obj.find('.ui-timepicker-input').spinner('value');
			}
		};
		
		/**
		 * Returns the formatted date and time.
		 * 
		 * @param	{date}		date
		 *   The date to format.
		 * @param	{boolean}	getDate
		 *   If the result should contain the result.
		 * @param	{boolean}	getTime
		 *   The the result should contain minutes and hours.
		 * @param	{string}	separator
		 *   Separator for the date. (optional, if not set '.')
		 *   
		 * @return	{string}
		 *   The formatted date and time.
		 */
		this.getFormattedTime = function(date, getDate, getTime, separator) {
			separator	= separator ? separator : '.';
			
			var year	= date.getFullYear();
			var month	= date.getMonth() + 1;
			var day		= date.getDate();
			var hours	= date.getHours();
			var minutes	= date.getMinutes();
			
			month	= month < 10 ? '0' + month : month;
			day		= day < 10 ? '0' + day : day;
			hours	= hours < 10 ? '0' + hours : hours;
			minutes	= minutes < 10 ? '0' + minutes : minutes;
			
			var dmy	= day + separator + month + separator + year;
			
			if(separator == '/') {
				dmy	= year + separator + month + separator + day;
			}
			
			var hm	= hours + ':' + minutes;
			
			var ret	= getDate ? dmy : '';
			
			if(getTime) {
				ret += getDate ? ' ' + hm : hm;
			}
			
			return ret;
		};
		
		/**
		 * Returns the options for the datetime picker.
		 * 
		 * @param	{mixed[]}	additional
		 *   Specific options for a single instance.
		 *   
		 * @return	{mixed[]}
		 *   The options.
		 */
		this.getDateTimePickerOptions = function(additional) {
			var opts = {
				controlType:		_withSpinners,
				currentText:		'Jetzt',
				closeText:			'Fertig',
				timeText:			'Zeit',
				hourText:			'Stunden',
				minuteText:			'Minuten',
				prevText:			'<',
				nextText:			'>',
				monthNames:			['Januar','Februar','März','April','Mai','Juni', 'Juli','August','September','Oktober','November','Dezember'],
				monthNamesShort:	['Jan', 'Feb', 'März', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sept', 'Okt', 'Nov', 'Dez'],
				dayNames:			['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'],
				dayNamesShort:		['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'],
				dayNamesMin:		['S','M','D','M','D','F','S'],
				dateFormat:			'dd.mm.yy',
				firstDay:			1,
				altFormat:			'yy/mm/dd',
				altFieldTimeOnly:	false
			};
			
			if(!additional) {
				additional = {};
			}
			
			$.extend(opts, additional);
			
			return opts;
		};
		
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
	
	/**
	 * Class for calendar operations.
	 */
	function _Cal() {
		/**
		 * Get all calendars of the user logged in.
		 * 
		 * @param	{function}	callback
		 *   Callback on success.
		 */
		this.fetchAll = function(callback) {
			var _callback = {
				success:	function(data) {
					var wrapper = $('<table />', {'id': 'calendar_list'});
					
					$(data).each(function(index, calendar) {
						var row = $('<tr />', {'class': 'calendar_list_row'}).appendTo(wrapper);
						$('<td />', {'class': 'calendar_color_hint'}).appendTo(row).css('background-color', '#' + calendar.color);
						$('<td />', {'class': 'calendar_item', 'title': calendar.description}).appendTo(row).text(calendar.name);
						row.click(function() { _this.Overlay.ShowDialogue.calendarRud(calendar.id, calendar.name) });
					});
					
					$('#calendar_list_box').empty().append(wrapper);
					
					if(callback) {
						callback(data);
					}
				}
			}
			
			var _request = {};
			
			_this.Helper.getJsonData('/calendar/list/', _request, _callback);
		};

		this.create = function() {
			var title	= 'Create calendar';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/new/', parent, function() {
					setTimeout(_this.Cal.fetchAll, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};

		this.show = function(calendarId) {
			var title	= 'Show calendar';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/view/' + calendarId, parent, function() {
					setTimeout(_this.Cal.fetchAll, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};

		this.edit = function(calendarId) {
			var title	= 'Edit calendar';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/edit/' + calendarId, parent, function() {
					setTimeout(_this.Cal.fetchAll, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};

		this.deleteCal = function(calendarId) {
			var title	= 'Delete calendar';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/delete/' + calendarId, parent, function() {
					setTimeout(_this.Cal.fetchAll, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};
		
		/**
		 * Grant a user permissions for a calendar.
		 * 
		 * @param	{int}		calId
		 *   Id of the calendar to grant permission.
		 * @param	{string}	email
		 *   Email of the user to grant permission.
		 * @param	{int}		permId
		 *   The id of the permission level.
		 */
		this.grantPermission = function(calendarId) {
			var title	= 'Share calendar';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/calshare/create/', parent, function() {
					setTimeout(_this.Cal.fetchAll, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};
	}
	
	/**
	 * Calendar operation functions.
	 */
	this.Cal = new _Cal;
	
	/**
	 * Calls for series operations.
	 */
	function _Series() {
		/**
		 * Create a new appointment (series).
		 */
		this.create = function() {
			var title	= 'Create series';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/series/create/', parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};

		this.show = function(appointmentId) {
			var title	= 'Show series';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/series/view/' + appointmentId, parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};

		this.edit = function(appointmentId) {
			var title	= 'Edit series';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/series/update/' + appointmentId, parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};
		
		/**
		 * Delete an appointment (series).
		 * 
		 * @param	{int}	id
		 *   The id of the series to delete.
		 */
		this.deleteSer = function(appointmentId) {
			var title	= 'Delete series';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/series/delete/' + appointmentId, parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};
	}
	
	/**
	 * Series operation functions.
	 */
	this.Series = new _Series;
	
	/**
	 * Class for series exception operations.
	 */
	function _Appointment() {
		/**
		 * Get all appointments in a specified time of the user logged in.
		 * 
		 * @param	{int}		sTime
		 *   Starttime of the series.
		 * @param	{int}		eTime
		 *   Endtime of the series.
		 * @param	{function}	callback
		 *   Callback to be run after the data is provided.
		 */
		this.fetchAll = function(fetchAfterDate, fetchBeforeDate, callback) {
			var _callback = {
				success:	function(data) {
					for(var i = 0; i < data.length; i++) {
						data[i] = JSON.parse(data[i]);
					}

					callback(data);
				}
			}
			
			var _request = {
				fetch_after_date:	fetchAfterDate,
				fetch_before_date:	fetchBeforeDate,
				calendar: 			1
			};
			
			_this.Helper.getJsonData('/calendar/appointment/list/', _request, _callback);
		};

		/**
		 * Get a single exception.
		 * 
		 * @param	{int}	seriesId
		 *   Id of the exception to fetch.
		 * @param	{int}	occurence
		 *   The number of the occurence of the exception.
		 */
		this.show = function(appointmentId) {
			var title	= 'Show appointment';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/appointment/view/' + appointmentId, parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};

		/**
		 * Get a single exception.
		 * 
		 * @param	{int}	seriesId
		 *   Id of the exception to fetch.
		 * @param	{int}	occurence
		 *   The number of the occurence of the exception.
		 */
		this.edit = function(appointmentId) {
			var title	= 'Edit appointment';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/appointment/update/' + appointmentId, parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};
		
		/**
		 * Create a new exception.
		 * 
		 * @param	{int}	seriesId
		 *   Id of the series of the exception.
		 * @param	{int}	occurence
		 *   Occurence of the exception in the series.
		 * @param	{int}	sTime
		 *   The starttime of the exception as UNIX timestamp.
		 * @param	{int}	eTime
		 *   The endtime of the exception of the series.
		 * @param	{int}	notes
		 *   Additional notes for the exception.
		 */
		this.create = function() {
			var title	= 'Create appointment';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/appointment/create/', parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};
		
		/**
		 * Delete an exception.
		 * 
		 * @param	{int}	seriesId
		 *   Id of the series the exception belongs to.
		 * @param	{int}	occurence
		 *   Occurence of the exception in the series.
		 */
		this.deleteApp = function(appointmentId) {
			var title	= 'Delete appointment';

			var callback = function(parent) {
				_this.Helper.getForm('/calendar/appointment/delete/' + appointmentId, parent, function() {
					setTimeout(_this.View.show, 500);
				});
			}
			
			_this.Overlay.show(title, null, callback);
		};
	}
	
	/**
	 * Series exception operation functions.
	 */
	this.Appointment = new _Appointment;
	
	/**
	 * Class for small calendar operations.
	 */
	function _SmallCal() {
		/**
		 * The date, the user has selected. Initial today.
		 */
		var _selectedDate = new Date();
		
		/**
		 * Stores the month and the year wich is actual shown.
		 */
		var _show = {
			 month:	_selectedDate.getMonth(),
			 year:	_selectedDate.getFullYear()
		};
		
		/**
		 * Storage for the day names.
		 */
		var _dayNames = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'];
		
		/**
		 * Storage for the month names.
		 */
		var _monthNames = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
		
		/**
		 * Returns the selected date.
		 * 
		 * @return	{date}
		 *   The selected date.
		 */
		this.getSelectedDate = function() {
			var date = new Date(_selectedDate.getTime());
			return date;
		};
		
		/**
		 * Returns the name of a day.
		 * 
		 * @return	{string}
		 *   The name of the day (starting bei 0).
		 */
		this.getDayName = function(nr) {
			while(nr < 0) {
				nr += 7;
			}
			
			while(nr >= 7) {
				nr -= 7;
			}
			
			return _dayNames[nr];
		};
		
		/**
		 * Returns the name of a month.
		 * 
		 * @return	{string}
		 *   The name of the month (starting bei 0).
		 */
		this.getMonthName = function(nr) {
			while(nr < 0) {
				nr += 12;
			}
			
			while(nr >= 12) {
				nr -= 12;
			}
			
			return _monthNames[nr];
		};
		
		/**
		 * Returns the days of the month of the actual selected day. Fills the first and last week
		 * with days of the previous / next month.
		 * 
		 * @param	{int}	monthNr
		 *   The number of the month, starting by 0.
		 * @param	{int}	monthYear
		 *   The year of the month.
		 * 
		 * @return	{mixed[]}
		 *   The days of the month.
		 *   Structure:
		 *   [{
		 *   	nr:			{int} the number of the day in the month,
		 *   	month:		{int} the number of the month (starting by 0),
		 *   	year:		{int} the actual year (as full year),
		 *   	active:		{boolaen} if the day is of the actual selected month,
		 *   	selected:	{boolean} if the day is the selected day
		 *   }]
		 */
		this.getMonthDays = function(monthNr, monthYear) {
			var monthDays = new Array();
			
			var iter = new Date(monthYear, monthNr, 1);
			
			if(iter.getDay() == 1) {
				iter.setDate(iter.getDate() - 7);
			} else if(iter.getDay() == 0) {
				iter.setDate(iter.getDate() - 6);
			} else {
				iter.setDate(iter.getDate() - iter.getDay() + 1);
			}
			
			for(var i = 0; i < 42; i++) {
				var day = {
					nr:			iter.getDate(),
					month:		iter.getMonth(),
					year:		iter.getFullYear(),
					active:		iter.getMonth() == monthNr,
					selected:	(iter.getMonth() == _selectedDate.getMonth() && iter.getDate() == _selectedDate.getDate())
				};
				
				monthDays.push(day);
				iter.setDate(iter.getDate() + 1);
			}
			
			return monthDays;
		};
		
		/**
		 * Create the little calendar.
		 */
		this.create = function() {
			var calendarTable = $('<table />', {'id': 'small_calendar_body', 'cellspacing': 2, 'cellpadding': 2});
			var monthDays = this.getMonthDays(_show.month, _show.year);
			var tableRow;
			
			for(var i = 0; i < monthDays.length; i++) {
				if(i % 7 == 0) {
					tableRow = $('<tr />').appendTo(calendarTable);
				}
				
				var itemClass = 'small_calendar_item';
				itemClass += !monthDays[i].active ? ' inactive' : '';
				itemClass += monthDays[i].selected ? ' selected' : '';
				
				var onclick = 'cal.SmallCal.setDate(' + monthDays[i].year + ', ' + monthDays[i].month + ', ' + monthDays[i].nr + ', true)';
				
				$('<td />', {'class': itemClass, 'onclick': onclick}).appendTo(tableRow).text(monthDays[i].nr);
			}
			
			var headHtml = '<span class="pointer" style="float:left;" onclick="cal.SmallCal.prevMonth();">&lt;</span>';
			headHtml += _monthNames[_show.month] + ' ' + _show.year;
			headHtml += '<span class="pointer" style="float:right;" onclick="cal.SmallCal.nextMonth();">&gt;</span>';
			var calendarHead = $('<div />', {'id': 'small_calendar_head'}).html(headHtml);

			$('#small_calendar_wrapper').empty().append(calendarHead).append(calendarTable);
		};
		
		/**
		 * Sets a date.
		 * 
		 * @param	{int}		year
		 *   The year to be shown.
		 * @param	{int}		month
		 *   The month to be shown.
		 * @param	{int}		day
		 *   The selected day.
		 * @param	{boolean}	jumpToDay
		 *   If the view should jump to day view. (optional, default false)
		 */
		this.setDate = function(year, month, day, jumpToDay) {
			_selectedDate = new Date(year, month, day);
			
			_show.year	= _selectedDate.getFullYear();
			_show.month = _selectedDate.getMonth();
			
			var type = jumpToDay ? 'day' : '';
			_this.View.show(type);
		};
		
		/**
		 * Shows the miniature calendar for the next month.
		 */
		this.nextMonth = function() {
			_show.month += 1;
			
			if(_show.month >= 12) {
				_show.month -= 12;
				_show.year++;
			}
			
			this.create();
		};
		
		/**
		 * Shows the miniature calendar for the previous month.
		 */
		this.prevMonth = function() {
			_show.month -= 1;
			
			if(_show.month < 0) {
				_show.month += 12;
				_show.year--;
			}
			
			this.create();
		};
	}
	
	/**
	 * Small calender operation functions.
	 */
	this.SmallCal = new _SmallCal;
	
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
		
		/**
		 * Class for showing dialogues.
		 */
		function _ShowDialogue() {
			/**
			 * Show dialog to choose between editing a series or a exception for the series.
			 * 
			 * @param	{int}	seriesId
			 *   Id of the series.
			 * @param	{int}	occurence
			 *   Occurence of the exception within the series.
			 */
			this.createSeriesOrAppointment = function(seriesId, occurence) {
				var title	= 'Bitte wählen';
				var content	= new Array();
				
				content.push($('<div />').text('Möchten sie einen Serietermin oder einen Einzeltermin anlegen?'));
				var buttonWrapper	= $('<div />', {'class': 'button_bar'});
				var series			= $('<input />', {'type': 'button', 'class': 'cal_form_button', 'value': 'Serie'}).appendTo(buttonWrapper);
				var appointment		= $('<input />', {'type': 'button', 'class': 'cal_form_button', 'value': 'Einzeltermin'}).appendTo(buttonWrapper);
				
				series.click(function() {
					_this.Series.create();
				});
				
				appointment.click(function() {
					_this.Appointment.create();
				});
				
				content.push(buttonWrapper);
				
				_this.Overlay.show(title, content);
			};

			this.seriesRud = function(appointmentId, appointmentName) {
				var title	= 'Bitte wählen';
				var content	= new Array();
				
				content.push($('<div />').text('Was möchten sie mit der Serie ' + appointmentName + ' machen?'));
				var buttonWrapper	= $('<div />', {'class': 'button_bar'});
				var show			= $('<input />', {'type': 'button', 'value': 'Show'}).appendTo(buttonWrapper);
				var edit			= $('<input />', {'type': 'button', 'value': 'Edit'}).appendTo(buttonWrapper);
				var deleteBtn		= $('<input />', {'type': 'button', 'value': 'Delete'}).appendTo(buttonWrapper);
				
				show.click(function() {
					_this.Series.show(appointmentId);
				});
				
				edit.click(function() {
					_this.Series.edit(appointmentId);
				});

				deleteBtn.click(function() {
					_this.Series.deleteSer(appointmentId);
				});
				
				content.push(buttonWrapper);
				
				_this.Overlay.show(title, content);
			};

			this.appointmentRud = function(appointmentId, appointmentName) {
				var title	= 'Bitte wählen';
				var content	= new Array();
				
				content.push($('<div />').text('Was möchten sie mit dem Termin ' + appointmentName + ' machen?'));
				var buttonWrapper	= $('<div />', {'class': 'button_bar'});
				var show			= $('<input />', {'type': 'button', 'value': 'Show'}).appendTo(buttonWrapper);
				var edit			= $('<input />', {'type': 'button', 'value': 'Edit'}).appendTo(buttonWrapper);
				var deleteBtn		= $('<input />', {'type': 'button', 'value': 'Delete'}).appendTo(buttonWrapper);
				
				show.click(function() {
					_this.Appointment.show(appointmentId);
				});
				
				edit.click(function() {
					_this.Appointment.edit(appointmentId);
				});

				deleteBtn.click(function() {
					_this.Appointment.deleteApp(appointmentId);
				});
				
				content.push(buttonWrapper);
				
				_this.Overlay.show(title, content);
			};

			this.calendarRud = function(calendarId, calendarName) {
				var title	= 'Bitte wählen';
				var content	= new Array();
				
				content.push($('<div />').text('Was möchten sie mit Kalender ' + calendarName + ' machen?'));
				var buttonWrapper	= $('<div />', {'class': 'button_bar'});
				var show			= $('<input />', {'type': 'button', 'value': 'Show'}).appendTo(buttonWrapper);
				var edit			= $('<input />', {'type': 'button', 'value': 'Edit'}).appendTo(buttonWrapper);
				var deleteBtn		= $('<input />', {'type': 'button', 'value': 'Delete'}).appendTo(buttonWrapper);
				var permissions		= $('<input />', {'type': 'button', 'value': 'Grant permissions'}).appendTo(buttonWrapper);
				
				show.click(function() {
					_this.Cal.show(calendarId);
				});
				
				edit.click(function() {
					_this.Cal.edit(calendarId);
				});

				deleteBtn.click(function() {
					_this.Cal.deleteCal(calendarId);
				});

				permissions.click(function() {
					_this.Cal.grantPermission(calendarId);
				});
				
				content.push(buttonWrapper);
				
				_this.Overlay.show(title, content);
			};
		}
		
		/**
		 * Dialog overlay functions.
		 */
		this.ShowDialogue = new _ShowDialogue;
	}
	
	/**
	 * Overlay functions.
	 */
	this.Overlay = new _Overlay();
	
	/**
	 * Class for functions for the view.
	 */
	function _View() {
		/**
		 * Storage for the view type. Possible values are day, week, month and list.
		 */
		var _type = 'day';
		
		/**
		 * Functions to create the views.
		 */
		var _create = new function() {
			/**
			 * Create the header with the names of the weekdays.
			 * 
			 * @return	{jQuery}
			 *   The header box.
			 */
			var _createDayHeader = function() {
				var dayHeadWrapper = $('#calendar_head');
				dayHeadWrapper.empty();
				dayHeadWrapper.css('display', '');
				$('#calendar_body').css('height', 'calc(100% - 35px)');
				
				for(var i = 0; i < 7; i++) {
					$('<div />', {'class': 'calendar_head_days'}).appendTo(dayHeadWrapper).text(_this.SmallCal.getDayName(i));
				}
			};
			
			/**
			 * Creates the table with the hours for the weekdays.
			 * 
			 * @return	{jQuery}
			 *   The table for the week.
			 */
			var _createWeekTable = function() {
				var weekTable = $('<table />', {'class': 'calendar_background_table'});
				
				for(var i = 0; i < 24; i++) {
					for(var j = 0; j < 4; j++) {
						var tr = $('<tr />', {'class': 'calendar_background_table_row'}).appendTo(weekTable);
						
						if(j == 0) {
							$('<td />', {'class': 'calendar_background_table_hours', 'rowspan': 4}).appendTo(tr).text(i + ':00');
						}
						
						for(var k = 0; k < 7; k++) {
							$('<td />', {'class': 'calendar_background_table_week_items'}).appendTo(tr);
						}
					}
				}
				
				$('#calendar_body').append(weekTable);
			};
			
			/**
			 * Creates the table for the day view.
			 * 
			 * @return	{jQuery}
			 *   The wrapper for the day table.
			 */
			this.day = function() {
				var dayTable = $('<table />', {'class': 'calendar_background_table'});
				
				for(var i = 0; i < 24; i++) {
					for(var j = 0; j < 4; j++) {
						var tr = $('<tr />', {'class': 'calendar_background_table_row'}).appendTo(dayTable);
						
						if(j == 0) {
							$('<td />', {'class': 'calendar_background_table_hours', 'rowspan': 4}).appendTo(tr).text(i + ':00');
						}
						
						$('<td />', {'class': 'calendar_background_table_day_items'}).appendTo(tr);
					}
				}
				
				$('#calendar_body').append(dayTable);
			};
			
			/**
			 * Creates the week view.
			 * 
			 * @return	{jQuery[]}
			 *   The day header and the week view.
			 */
			this.week = function() {
				_createDayHeader();
				_createWeekTable();
				
				var weekItemBox	= $('<div />', {'id': 'calendar_appointment_wrapper'}).appendTo($('#calendar_body'));
				
				for(var i = 0; i < 7; i++) {
					$('<div />', {'class': 'calendar_items_rows'}).appendTo(weekItemBox);
				}
			};
			
			/**
			 * Create the month view.
			 * 
			 * @return	{jQuery[]}
			 *   The day table and the month view.
			 */
			this.month = function() {
				_createDayHeader();

				var monthItemBox	= $('<div />', {'id': 'calendar_month_item_wrapper'}).appendTo($('#calendar_body'));
				
				var selectedDate	= _this.SmallCal.getSelectedDate();
				var monthDays		= _this.SmallCal.getMonthDays(selectedDate.getMonth(), selectedDate.getFullYear());
				
				for(var i = 0; i < monthDays.length; i++) {
					var itemClass = 'calendar_month_item ' + (monthDays[i].active ? '' : 'inactive');
					var monthItem = $('<div />', {'class': itemClass}).appendTo(monthItemBox);
					$('<div />', {'class': 'calendar_month_item_content'}).appendTo(monthItem);
					$('<div />', {'class': 'calendar_month_item_label'}).appendTo(monthItem).text(monthDays[i].nr);
				}
			};
		}
		
		/**
		 * Functions to update the view data.
		 */
		var _update = new function() {
			/**
			 * Sort the days.
			 * 
			 * @param	{mixed[]}	data
			 *   The day data.
			 * 
			 * @return	{mixed[][]}
			 *   A sorted array of the days.
			 */
			var _sortDay = function(data) {
				var dates = new Array();
				
				for(var i = 0; i < data.length; i++) {
					for(var j = 0; j <= dates.length; j++) {
						if(j < dates.length) {
							var len = dates[j].length - 1;
							
							if(data[i].starttime >= dates[j][len].endtime) {
								dates[j].push(data[i]);
								break;
							}
						} else {
							dates.push(new Array());
							dates[j].push(data[i]);
							break;
						}
					}
				}
				
				return dates;
			};

			var _addRudLink = function(item, appointmentId, appointmentName, isSeries) {
				if(isSeries) {
					item.click(function() { _this.Overlay.ShowDialogue.seriesRud(appointmentId, appointmentName); });
				} else {
					item.click(function() { _this.Overlay.ShowDialogue.appointmentRud(appointmentId, appointmentName); });
				}
			}
			
			/**
			 * Update the day view.
			 * 
			 * @param	{mixed[]}	data
			 *   The data to show.
			 */
			var _updateDay = function(data) {
				var dates = _sortDay(data);
				
				var maxParallel = dates.length;
				var box = $('<div />', {'id': 'calendar_appointment_wrapper'}).appendTo($('#calendar_body'));
				
				for(var i = 0; i < maxParallel; i++) {
					var wrapper = $('<div />', {'class': 'calendar_appointment_column'}).appendTo(box);
					wrapper.css('width', 100 / maxParallel + '%');
					
					$(dates[i]).each(function(index, date) {
						var marker	= '<div class="marker" style="background-color: #' + date.color + ';"></div>';
						var name	= '<span class="name">' + date.name + '</span>';
						var notes	= date.notes ? date.notes : '';
						var notes_l = '';
						
						if(notes.length > 40) {
							notes_l	= notes;
							notes	= notes.substr(0, 40) + '...';
						}
						
						notes		= notes != '' ? '<br><span class="notes"' + (notes_l != '' ? (' title="' + notes_l + '"') : '') + '>' + notes + '</span>' : '';
						
						var start	= new Date(date.starttime * 1000);
						var top		= start.getHours() * 60 + start.getMinutes();
						var height	= (date.endtime - date.starttime) / 60;
						
						var dateItem = $('<div />', {'class': 'calendar_appointment shadow_outer'}).appendTo(wrapper).html(marker + name + notes);
						dateItem.css({'top': top + 'px', 'height': height + 'px'});7
						
						_addRudLink(dateItem, date.appointment_id, date.name, date.series);
					});
				}
			};
			
			/**
			 * Update the week view.
			 * 
			 * @param	{mixed[]}	data
			 *   The data to show.
			 */
			var _updateWeek = function(data) {
				var dataPerDay = new Array();
				
				for(var i = 0; i < 7; i++) {
					dataPerDay.push(new Array());
				}
				
				for(var i = 0; i < data.length; i++) {
					var index = (new Date(data[i].starttime * 1000)).getDay();
					index--;
					index = index < 0 ? index + 7 : index;
					dataPerDay[index].push(data[i]);
				}
				
				for(var k = 0; k < dataPerDay.length; k++) {
					var dates = _sortDay(dataPerDay[k]);
					
					var maxParallel = dates.length;
					var box = $('.calendar_items_rows:nth-child(' + (k + 1) + ')');
					
					for(var i = 0; i < maxParallel; i++) {
						var wrapper = $('<div />', {'class': 'calendar_appointment_column'}).appendTo(box);
						wrapper.css('width', 100 / maxParallel + '%');
						
						$(dates[i]).each(function(index, date) {
							var marker	= '<div class="marker" style="background-color: #' + date.color + ';"></div>';
							var name	= '<span class="name">' + date.name + '</span>';
							var notes	= date.notes ? date.notes : '';
							var notes_l	= '';
							
							if(notes.length > 40) {
								notes_l	= notes;
								notes	= notes.substr(0, 40) + '...';
							}
							
							notes		= notes != '' ? '<br><span class="notes"' + (notes_l != '' ? (' title="' + notes_l + '"') : '') + '>' + notes + '</span>' : '';
							
							var start	= new Date(date.starttime * 1000);
							var top		= start.getHours() * 60 + start.getMinutes();
							var height	= (date.endtime - date.starttime) / 60;
							
							var dateItem = $('<div />', {'class': 'calendar_appointment shadow_outer'}).appendTo(wrapper).html(marker + name + notes);
							dateItem.css({'top': top + 'px', 'height': height + 'px'});
							
							_addRudLink(dateItem, date.appointment_id, date.name, date.series);
						});
					}
				}
			};
			
			/**
			 * Update the month view.
			 * 
			 * @param	{mixed[]}	data
			 *   The data to show.
			 */
			var _updateMonth = function(data) {
				var dataPerDay = new Array();
				
				for(var i = 0; i < 31; i++) {
					dataPerDay.push(new Array());
				}
				
				for(var i = 0; i < data.length; i++) {
					var index = (new Date(data[i].starttime * 1000)).getDate() - 1;
					dataPerDay[index].push(data[i]);
				}
				
				for(var i = 0; i < dataPerDay.length; i++) {
					var box = $('.calendar_month_item:not(.inactive):eq(' + i + ') .calendar_month_item_content');
					
					$(dataPerDay[i]).each(function(index, date) {
						var start	= new Date(date.starttime * 1000);
						var end		= new Date(date.endtime * 1000);
						var marker	= '<div class="marker" style="background-color: #' + date.color + ';"></div>';
						var time	= '<span class="time">' + _this.Helper.getFormattedTime(start, false, true) + ' - ' + _this.Helper.getFormattedTime(end, false, true) + '</span>';
						var name	= '<br><span class="name">' + date.name + '</span>';
						var notes	= date.notes ? date.notes : '';
						
						var dateItem = $('<div />', {'class': 'month_item_content_date', 'title': notes}).appendTo(box).html(marker + time + name);
						
						_addRudLink(dateItem, date.appointment_id, date.name, date.series);
					});
				}
			};
			
			/**
			 * Update the list view.
			 * 
			 * @param	{mixed[]}	data
			 *   The data to show.
			 */
			var _updateList = function(data) {
				var calBox		= $('#calendar_body');
				var listPrev	= $('<div />', {'id': 'calendar_list_prev'}).appendTo(calBox);
				var listContent	= $('<div />', {'id': 'calendar_list_content'}).appendTo(calBox);
				var listNext	= $('<div />', {'id': 'calendar_list_next'}).appendTo(calBox);
				
				$(data).each(function(index, date) {
					var start	= new Date(date.starttime * 1000);
					var end		= new Date(date.endtime * 1000);
					
					var marker		= '<div class="marker" style="background-color: #' + date.color + ';"></div>';
					var time		= '<span class="time">' + _this.Helper.getFormattedTime(start, true, true) + ' - ' + _this.Helper.getFormattedTime(end, false, true) + '</span>';
					var name		= '<br><span class="name">' + date.name + '</span>';
					var notes		= date.notes ? '<br><span class="notes">' + date.notes + '</span>' : '';

					var dateDiv = $('<div />', {'class': 'calendar_list_item'}).appendTo(listContent).html(marker + time + name + notes);
					
					_addRudLink(dateDiv, date.appointment_id, date.name, date.series);
				});
			};
			
			/**
			 * Update the actual view.
			 */
			this.general = function() {
				var selected	= _this.SmallCal.getSelectedDate();
				var text		= '';
				
				if(_type == 'day' || _type == 'week') {
					$('#calendar_body').animate({scrollTop: 420}, 0);
				}
				
				switch(_type) {
					case 'week':
						selected.setDate(selected.getDate() - selected.getDay() + 1);
						var day		= selected.getDate() < 10 ? '0' + selected.getDate() : selected.getDate();
						var month	= selected.getMonth() < 9 ? '0' + (selected.getMonth() + 1) : (selected.getMonth() + 1);
						var year	= selected.getFullYear();
						text		= day + '.' + month + '.' + year + ' - ';
						var sTime = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate(), 0, 0, 0);
						
						selected.setDate(selected.getDate() + 6);
						day			= selected.getDate() < 10 ? '0' + selected.getDate() : selected.getDate();
						month		= selected.getMonth() < 9 ? '0' + (selected.getMonth() + 1) : (selected.getMonth() + 1);
						year		= selected.getFullYear();
						text		+= day + '.' + month + '.' + year;
						var eTime = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate() + 1, 0, 0, 0);
						
						_this.Appointment.fetchAll(sTime, eTime, _updateWeek);
					  break;
					
					case 'month':
						text = _this.SmallCal.getMonthName(selected.getMonth()) + ' ' + selected.getFullYear();
						
						var sTime = new Date(selected.getFullYear(), selected.getMonth(), 1, 0, 0, 0);
						var eTime = new Date(selected.getFullYear(), selected.getMonth() + 1, 1, 0, 0, 0);
						
						_this.Appointment.fetchAll(sTime, eTime, _updateMonth);
					  break;
					
					case 'list':
						text = '';
						
						var sTime = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate(), 0, 0, 0);
						var eTime = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate() + 30, 0, 0, 0);
						
						_this.Appointment.fetchAll(sTime, eTime, _updateList);
					  break;
					
					default:
						var day		= selected.getDate() < 10 ? '0' + selected.getDate() : selected.getDate();
						var month	= selected.getMonth() < 9 ? '0' + (selected.getMonth() + 1) : (selected.getMonth() + 1);
						var year	= selected.getFullYear();
						
						text = day + '.' + month + '.' + year;
						
						var sTime = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate(), 0, 0, 0);
						var eTime = new Date(selected.getFullYear(), selected.getMonth(), selected.getDate() + 1, 0, 0, 0);
						
						_this.Appointment.fetchAll(sTime, eTime, _updateDay);
					  break;
				}
				
				$('#info_line').text(text);
			};
		};
		
		/**
		 * Returns the type of the actual created view.
		 * 
		 * @return	{string}
		 *   The type of the view.
		 */
		this.getType = function() {
			return _type;
		};
		
		/**
		 * Create a new view.
		 * 
		 * @param	{string}	type
		 *   The type of the view. Possible are day, week, month and list. (optional, if not set: no change).
		 */
		this.show = function(type) {
			if(type) {
				_type = type;
			}
			
			$('.submenu .menu_item').removeClass('active');
			$('#view_selector_' + _type).addClass('active');
			$('#calendar_body').empty().css('height', 'calc(100% - 5px)');
			$('#calendar_head').css('display', 'none');

			
			switch(_type) {
				case 'week':
					_create.week();
				  break;
				
				case 'month':
					_create.month();
				  break;
				
				case 'list':
				  break;
				
				default:
					_create.day();
				  break;
			}
			
			_this.SmallCal.create();
			
			_update.general();
		};
		
		/**
		 * Sets the view to today.
		 */
		this.setToday = function() {
			var now = new Date();
			_this.SmallCal.setDate(now.getFullYear(), now.getMonth(), now.getDate());
		};
		
		/**
		 * Sets the view to one selection before (e.g. week -> last week, month -> last month).
		 */
		this.setPrev = function() {
			var selected	= _this.SmallCal.getSelectedDate();
			var year		= selected.getFullYear();
			var month		= selected.getMonth();
			var day			= selected.getDate();
			
			switch(_type) {
				case 'week':
					_this.SmallCal.setDate(year, month, day - 7);
				  break;
				
				case 'month':
					var tmp			= new Date(year, month - 1, day);
					
					while(tmp.getMonth() == month) {
						tmp.setDate(tmp.getDate() - 1);
					}
					
					_this.SmallCal.setDate(tmp.getFullYear(), tmp.getMonth(), tmp.getDate());
				  break;
				
				case 'list':
//						░░░░░▄▄▄▄▄▄░░░░░░░░░░
//						░░▄█▀░░░░░▄▀▄░░░░░░░░
//						░█░▀▀▀▀▀▀▀▀░░█▄░░░░░░
//						█▀░░░░░░░░░░░░█░░░░░░
//						█░░░░░░░░░░░░░█░░░░░░
//						▀█░░░░░░░░░░░░█░░░░░░
//						░▀▄░░░░░░░░░▄█░░░░░░░
//						░░░▀█▄▄▄▄▄▄██▄▄░░░░░░
//						░░▄▄█▀███▀██████░░░░░
//						░░▀██░░██▀█████▄▄░░░░
//						░░░░░░░░░░▄▄███▀█▄▀▄░
//						░░▄█▄▄▄██████▀▄▀▄▀█▄▀
//						░██░░░▀██▀░░░░░░▄▀▄█░
//						░█▄░░░░░█▄░░░░░░░▀░░░
//						░░▀█▄░░░░▀▀▀░░░░░░░░░
//						Nothing to do here!!!
				  break;
				
				default:
					_this.SmallCal.setDate(year, month, day - 1);
				  break;
			}
		};
		
		/**
		 * Sets the view to one selection before (e.g. week -> next week, month -> next moth).
		 */
		this.setNext = function() {
			var selected	= _this.SmallCal.getSelectedDate();
			var year		= selected.getFullYear();
			var month		= selected.getMonth();
			var day			= selected.getDate();
			
			switch(_type) {
				case 'week':
					_this.SmallCal.setDate(year, month, day + 7);
				  break;
				
				case 'month':
					var tmp			= new Date(year, month + 1, day);
					
					while(tmp.getMonth() == (month + 2) % 12) {
						tmp.setDate(tmp.getDate() - 1);
					}
					
					_this.SmallCal.setDate(tmp.getFullYear(), tmp.getMonth(), tmp.getDate());
				  break;
				
				case 'list':
//						░░░░░▄▄▄▄▄▄░░░░░░░░░░
//						░░▄█▀░░░░░▄▀▄░░░░░░░░
//						░█░▀▀▀▀▀▀▀▀░░█▄░░░░░░
//						█▀░░░░░░░░░░░░█░░░░░░
//						█░░░░░░░░░░░░░█░░░░░░
//						▀█░░░░░░░░░░░░█░░░░░░
//						░▀▄░░░░░░░░░▄█░░░░░░░
//						░░░▀█▄▄▄▄▄▄██▄▄░░░░░░
//						░░▄▄█▀███▀██████░░░░░
//						░░▀██░░██▀█████▄▄░░░░
//						░░░░░░░░░░▄▄███▀█▄▀▄░
//						░░▄█▄▄▄██████▀▄▀▄▀█▄▀
//						░██░░░▀██▀░░░░░░▄▀▄█░
//						░█▄░░░░░█▄░░░░░░░▀░░░
//						░░▀█▄░░░░▀▀▀░░░░░░░░░
//						Nothing to do here!!!
				  break;
				
				default:
					_this.SmallCal.setDate(year, month, day + 1);
				  break;
			}
		};
	}
	
	/**
	 * Functions for the view.
	 */
	this.View = new _View;
}