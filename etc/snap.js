var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

if (system.args.length < 3 || system.args.length > 7) {
    console.log('Usage: snap.js URL filename width height timeout');
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];
    page.viewportSize = page.clipRect = { width: system.args[3], height: system.args[4] };
    page.customHeaders = {'Referer': address};
    page.settings.javascriptEnabled = true;
    page.settings.localToRemoteUrlAccessEnabled = true;
    page.settings.XSSAuditingEnabled = true;
    page.settings.webSecurityEnabled = true;
    page.settings.ignoreSslErrors = true; /* need this for our private certs */
    page.settings.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36';
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit();
        } else {
            window.setTimeout(function () {
                page.render(output);
                phantom.exit();
            }, system.args[5]);
        }
    });
}