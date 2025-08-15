# API de Integración

La aplicación expone una API HTTP basada en Flask para integrarse con
plataformas externas como sistemas de e-commerce o CRM.

## Autenticación

Los ejemplos asumen que se utiliza una pasarela de pago externa que requiere
un `api_key` configurado en el servidor.

## Endpoints

### `POST /api/payments`
Realiza un cobro para una factura y registra el pago.

```json
{
  "factura_id": 1,
  "monto": 100.0
}
```

### `POST /api/warranties`
Registra una reclamación de garantía para una reparación.

```json
{
  "reparacion_id": 1,
  "descripcion": "Falla de pantalla"
}
```

### `GET /api/warranties`
Lista todas las garantías registradas.

### `POST /api/returns`
Registra una devolución asociada a una factura.

```json
{
  "factura_id": 1,
  "motivo": "Producto defectuoso"
}
```

### `GET /api/returns`
Lista las devoluciones registradas.

## Flujos de integración
1. El sistema externo crea una reparación y factura.
2. Para cobrar en línea, envía los datos de la factura a `POST /api/payments`.
3. Si el cliente presenta una falla cubierta por garantía, registra el evento en
   `POST /api/warranties`.
4. Para devoluciones de productos facturados, usar `POST /api/returns`.
