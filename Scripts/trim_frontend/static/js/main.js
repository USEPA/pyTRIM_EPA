
// Add Polyfills

// https://developer.mozilla.org/en-US/docs/Web/API/Element/closest
if (!Element.prototype.matches) {
  Element.prototype.matches = Element.prototype.msMatchesSelector || 
                              Element.prototype.webkitMatchesSelector;
}
if (!Element.prototype.closest) {
  Element.prototype.closest = function(s) {
    var el = this;

    do {
      if (el.matches(s)) return el;
      el = el.parentElement || el.parentNode;
    } while (el !== null && el.nodeType === 1);
    return null;
  };
}

// Add global functions

/*
 * Calculate the distance between two dates;
 * returns an array of human-readable durations
 * (by default, ['years', 'days', 'hours', 'minutes'])
 */
function calculateDateDistance(start, end, funcs) {
    if (funcs == undefined) {
        funcs = ['years', 'days', 'hours', 'minutes'];
    }

    start = moment.utc(start);
    end = moment.utc(end).add(1, 'days');

    var diff = [];
    for (var i = 0, len = funcs.length; i < len; i++) {
        var func = funcs[i];

        var val = end.diff(start, func);
        start.add(val, func);
        if (val > 1) {
            diff.push(val + ' ' + func);
        }
        else if (val > 0) {
            diff.push(val + ' ' + func.slice(0, -1));
        }
    }
    return diff;
}

// does not refresh parcels
function getParcelByKey(key, val) {
    return TRIM.store.currentScenario.parcels.filter(e=>e[key]==val)[0]
}

// Add global objects

// An ajax handler
window.AJAX = (function(ajax) {

    ajax.call = function(opts) {

        var method = opts.method || 'GET';
        var url = opts.url || window.location.pathname;
        var data = opts.data || null;

        var request = new XMLHttpRequest();

		var callback = opts.callback || undefined;

		request.addEventListener("readystatechange", () => {
		  if (request.readyState === 4 && request.status === 200) {
			  let parsedResponseData = null;
			  try {
				  parsedResponseData = JSON.parse(request.responseText);
			  } catch (e) {
				  parsedResponseData = request.responseText;
			  }

			if (callback !== undefined) { callback(true, parsedResponseData); }
		  } else if (request.readyState === 4) {
		    if (callback !== undefined) { callback(false, "could not fetch the data"); }
		  }
		});

        request.open(method, url);
        request.send(data);

        request.addEventListener('load', function() {
            try {
                this.responseJSON = JSON.parse(this.responseText);
            }
            catch {
                this.responseJSON = null;
            }
        });

        var wrapper = {};
        wrapper['on'] = function(event, func) {
            request.addEventListener(event, func);
            return wrapper;
        };
        return wrapper;
    };

    return ajax;
})(window.AJAX || {})

// A loading-screen handler
window.LoadingScreen = (function(loader) {
    function makeLoadingElement() {
        // Grab the body element
        var body = document.getElementsByTagName('body')[0];

        var loader = document.createElement('div');
        loader.style.display = 'none';
        loader.className = 'loading-screen';

        var screen = document.createElement('div');
        screen.className = 'blocking-screen';
        loader.append(screen);

        var xPositioner = document.createElement('div');
        xPositioner.className = 'row mx-0 h-100 text-center';
        screen.append(xPositioner);

        var yPositioner = document.createElement('div');
        yPositioner.className = 'col-sm align-self-center';
        xPositioner.append(yPositioner);

        var spinnerSize = '6rem';
        var spinnerWidth = '0.75em';
        var spinner = document.createElement('div');
        spinner.className = 'spinner-border text-primary';
        spinner.setAttribute('role', 'status');
        spinner.style.borderWidth = spinnerWidth;
        spinner.style.width = spinnerSize;
        spinner.style.height = spinnerSize;
        yPositioner.append(spinner);

        var txt = document.createElement('span');
        txt.className = 'sr-only';
        txt.innerText = 'Loading ...'
        spinner.append(txt);

        body.append(loader);

        return loader;
    }

    // Grab the dom element for the loading screen,
    // Or create it if it doesn't exist
    var loaderElement = document.getElementsByClassName('loading-screen');
    if (loaderElement.length) {
        loaderElement = loaderElement[0];
    }
    else {
        loaderElement = makeLoadingElement();
    }

    // Keep track of how many loading requests have been made
    var loadingRequests = [];

    // Show the loading element
    function showLoader() {
        if (!loadingRequests.length) {
            return;
        }

        if (document.readyState === 'complete') {
            loaderElement.style.display = '';
        }
        else {
            setTimeout(showLoader, 200);
        }
    }
    // Hide the loading element
    function hideLoader() {
        if (loadingRequests.length) {
            return;
        }

        if (document.readyState === 'complete') {
            loaderElement.style.display = 'none';
        }
        else {
            setTimeout(hideLoader, 200);
        }
    }

    // Show the loading screen for a specific (or generic) reason
    loader.show = function(reason) {
        // Log an active loading request
        loadingRequests.push(reason || 1);
        // Ask the loader to show if appropriate
        showLoader();
    };
    // Hide the loading screen that was raised for a specific
    // (or generic) reason
    loader.hide = function(reason) {
        // Clear the loading request that was made for this reason
        var i = loadingRequests.indexOf(reason || 1);
        while (i !== -1) {
            loadingRequests.splice(i, 1);
            i = loadingRequests.indexOf(reason || 1);
        }
        // Ask the loader to hide if appropriate
        hideLoader();
    };
    // Force the loading screen to go away,
    // clearing all loading requests
    loader.resetUnsafe = function(reason) {
        // Invalidate all loading requests
        loadingRequests = [];
        // Ask the loader to hide
        hideLoader();
    };

    loader.why = function() {
        console.log([...loadingRequests]);
    }

    return loader;
})(window.LoadingScreen || {});

// Initialize global event-handlers

onDomLoad(function() {
    // window.LoadingScreen.show()
    // Register actions on body click
    document.body.addEventListener('click', function(e) {
        if (typeof(e.target.className)=="string") {
            var classes = e.target.className.split(' ');

            // Form text (in labels, specifically) shouldn't highlight
            // the field when clicked
            if (classes.indexOf('form-text') > -1) {
                e.preventDefault();
            }
        }
    });
});
