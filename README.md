# pandas-conditional-validator

Herramienta ligera para validar `DataFrame` de pandas en base a reglas
definidas en un archivo YAML. Las reglas pueden ser globales o aplicarse
únicamente a un parámetro (valor de la columna `parametro`).

## Configuración de reglas

Las reglas se definen en un archivo YAML. A partir de esta versión la sección
`parametros` acepta una **lista** de objetos, donde cada entrada especifica el
nombre del parámetro de forma explícita mediante la clave `name` (o `parametro`).
Esto evita la ambigüedad sobre si el identificador corresponde a una columna o
al valor de un parámetro dentro del `DataFrame`.

```yaml
parametros:
  - name: Relacion_NP
    condition:
      type: conditional
      if:
        operator: AND
        conditions:
          - type: greater_than
            col: nitrógeno
            value: 5
          - operator: OR
            conditions:
              - type: less_than
                col: fósforo
                value: 3
              - type: between
                col: fósforo
                min: 4
                max: 6
      then:
        type: less_than
        col: valor
        value: 2

_global:
  - type: between
    col: temperatura
    min: 0
    max: 35
```

La estructura anterior sigue siendo compatible con la sintaxis previa basada en
diccionarios, por lo que los archivos existentes continúan funcionando sin
modificaciones.