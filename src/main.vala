


int main (string[] argv) {
    // Create a new application
    var app = new Gtk.Application ("com.github.rafaelrpq.devOps",
                                   GLib.ApplicationFlags.FLAGS_NONE);

    app.activate.connect (() => {
        var window = new Gtk.ApplicationWindow (app);
        window.set_default_size (1024, 576);

        
        var url = "https://api.openf1.org/v1/drivers?&session_key=latest";

        var session = new Soup.Session ();
        var msg = new Soup.Message ("GET", url);


        var grid = new Gtk.Grid ();
        grid.margin_bottom = 10;
        grid.margin_end    = 10;
        grid.margin_start  = 10;
        grid.margin_top    = 10;

        grid.row_spacing   = 5;

        window.set_child (grid);

        session.queue_message (msg, (sess, mess) => {
            var status = new Gtk.Label ("Status Code: %u\n".printf (mess.status_code));
            var len    = new Gtk.Label ("Message length: %lld\n".printf (mess.response_body.length));
            var data   = new Gtk.Label ("");


            grid.attach (status, 1,1);
            grid.attach (len, 1,2);
            grid.attach (data, 1, 3);

            try {
                var node = Json.from_string ((string) mess.response_body.data);

                var nodes = node.get_array ().get_elements ();

                nodes.foreach (i => {
                    var driver = Json.gobject_deserialize (typeof (Driver), i) as Driver;

                    print ("%s\n",driver.full_name);
                });

            } catch (Error e) {
                print ("[ Error ]: %s\n", e.message);
            }
            //  print ((string) mess.response_body.data);
        });


        window.present ();
    });


    return app.run (argv);
}