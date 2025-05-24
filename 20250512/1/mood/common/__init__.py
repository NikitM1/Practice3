import cowsay
import io

# flake8: noqa W605
JGSBAT = cowsay.read_dot_cow(io.StringIO("""
$the_cow = <<EOC;
$thoughts
 $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC

"""))