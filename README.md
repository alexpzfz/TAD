# 1er Taller Avanzado DESI

15 y 16 de Agosto de 2023

Introducción a cosmodesi & desilike.

**Bloque0** (Alejandro): Introducción a cosmodesi (cosmoprimo, pypower, pycorr) y clustering fits con desilike.

**Bloque1** (Cristhian & Leonel): Introducción a cobaya y getdist.

**Bloque2** (Cristhian & Leonel): Interfaz deslike/cobaya, constricción de parámetros cosmológicos.




## Instalación local de cosmodesi
Instalar un ambiente nuevo en conda utilizando el archivo proporcionado:
```
conda env create -f cosmodesi_env.yml
```
Activar el ambiente de la siguiente forma:
```
conda activate cosmodesi
```

Si después de instalar el ambiente con las instrucciones anteriores, sigue habiendo errores con los notebooks porque no se instalaron correctamente cosmoprimo/desilike/cobaya/classy, como ya tenemos el resto de las dependencias es fácil y rápido instalar estos paquetes restantes más artesanalmente:

```
python -m pip install git+https://github.com/cosmodesi/cosmoprimo#egg=cosmoprimo[class,camb,astropy,extras]
python -m pip install git+https://github.com/cosmodesi/desilike#egg=desilike[plotting,jax]
python -m pip install cobaya --upgrade

git clone https://github.com/lesgourg/class_public.git
cd class_public
make
pip install . --user
```