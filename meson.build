project ('com.github.rafaelrpq.devOps', 'vala', 'c', version: '0.1.0')

sources = [
    'src/main.vala',
    'src/Driver.vala',
]

executable (
    meson.project_name (),

    sources,

    dependencies : [
        dependency  ('gtk4'),
        dependency  ('libsoup-2.4'),
        dependency  ('json-glib-1.0'),
    ],

    install : false,
)
