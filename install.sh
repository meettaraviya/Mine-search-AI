sudo apt-get install ocaml opam m4

opam init   # must be performed before installing opam packages
eval `opam config env`     # optional: add this line to your .bashrc
# The former state can be restored with: opam switch import "~/.opam/system/backup/state-20200319234725.export"
opam install ounit core ppx_sexp_conv sexplib core_bench menhir ppx_deriving camlidl ocamlbuild

git clone https://github.com/SHoltzen/mlcuddidil

cd mlcuddidil/
./configure && make && make install
cd ..

git clone https://github.com/SHoltzen/dice
cd dice
make
make test
cd ..