/* webshark */

jQuery.fn.center = function(parent) {
    if (parent) {
        parent = this.parent();
    } else {
        parent = window;
    }
    parent = $("#listing").get()
    this.css({
        "position": "absolute",
        "top": ((($(parent).height() - this.outerHeight()) / 2) + $(parent).scrollTop() + "px"),
        "left": ((($(parent).width() - this.outerWidth()) / 2) + $(parent).scrollLeft() + "px")
    });
    return this;
}

function init_trace() {
    var t = new Trace(TRACE_ID)
    t.fetch_listing(0, 10)
}

function Trace(id) {
    this.id = id
}

Trace.prototype.fetch_listing = function(start, count) {
    $("#loading").show()
    //$("#loading").center(true)
    var url = "packet-"+start+"-"+count
    $.getJSON(url, '', function(data) {
        var t = data['packets']
        var s = ''
        for (var i = 0; i < t.length; i++) {
            s += '<tr><td>'+ (t[i].join('</td><td>')) + '</td></tr>' + "\n"
        }

        $("#listing_table tr:last").after(s)
        //alert("fetch ok "+t.length+' elements')
        $("#loading").hide()
    })
}

Trace.prototype.fetch_detail = function(pid) {

}
