select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    coalesce(sum(i.price), 0) as total_item_price,
    coalesce(sum(i.freight_value), 0) as total_freight,
    coalesce(sum(i.price + i.freight_value), 0) as total_order_value
from {{ ref('stg_orders') }} o
inner join {{ ref('stg_order_items') }} i on o.order_id = i.order_id
group by 1, 2, 3, 4
