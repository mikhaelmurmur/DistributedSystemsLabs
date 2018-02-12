extern crate postgres;

use postgres::{Connection, TlsMode};
use postgres::params::{ConnectParams, Host};


struct Person {
    id: i32,
    name: String,
    data: Option<Vec<u8>>,
}

fn main() {

    let user_password : Option<&str> = Some("QAZxswedc123-");
    let host_addr = std::string::String::from("<connectionstring>");

    let params = ConnectParams::builder()
    .user("<Username>",user_password)
    .build(Host::Unix(host_addr));

    let conn = Connection::connect(params, TlsMode::None).unwrap();
    conn.execute("CREATE TABLE person (
                    id              SERIAL PRIMARY KEY,
                    name            VARCHAR NOT NULL,
                    data            BYTEA
                  )", &[]).unwrap();

    let me = Person {
        id: 0,
        name: "Steven".to_string(),
        data: None,
    };

    conn.execute("INSERT INTO person (name, data) VALUES ($1, $2)",
                 &[&me.name, &me.data]).unwrap();
    for row in &conn.query("SELECT id, name, data FROM person", &[]).unwrap() {
        let person = Person {
            id: row.get(0),
            name: row.get(1),
            data: row.get(2),
        };
        println!("Found person {}", person.name);
    }
}