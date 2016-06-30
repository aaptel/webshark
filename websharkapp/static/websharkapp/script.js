/* webshark */

function init_trace() {
    var t = new Trace(TRACE_ID)
    t.fetch_listing(0, 10)
}

function Trace(id) {
    this.id = id
}

Trace.prototype.fetch_listing = function(start, count) {
    $("#loading").show()
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
