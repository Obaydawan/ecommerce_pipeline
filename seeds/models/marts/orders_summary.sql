select
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    sum(i.price) as total_item_price,
    sum(i.freight_value) as total_freight,
    sum(i.price + i.freight_value) as total_order_value
from {{ ref('stg_orders') }} o
left join {{ ref('stg_order_items') }} i on o.order_id = i.order_id
group by 1, 2, 3, 4
