# pandas-conditional-validator

Herramienta ligera para validar `DataFrame` de pandas en base a reglas
definidas en un archivo YAML. Las reglas pueden ser globales o aplicarse
únicamente a un parámetro (valor de una columna cuyo nombre debe
indicarse mediante el argumento `param_col`).

## Configuración de reglas

Las reglas se definen en un archivo YAML. La sección `parametros` utiliza un
**objeto** donde cada clave corresponde al nombre de la regla mayor. Este nombre
debe coincidir con los valores de la columna indicada por `param_col` en el
`DataFrame`.

```yaml
parametros:
  Relacion_NP:
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

Cada clave dentro de `parametros` representa una regla que se aplicará a las
filas cuyo valor en la columna de parámetros coincida con ella.

## Uso de `validate_dataframe`

Al momento de validar un `DataFrame` se debe indicar explícitamente la
columna que contiene el nombre del parámetro mediante el argumento
`param_col`:

```python
from df_rule_validator.validator import validate_dataframe

fails, df_validado = validate_dataframe(df, rules, param_col="mi_columna")
```

`param_col` es obligatorio; la función no define un valor por defecto.

