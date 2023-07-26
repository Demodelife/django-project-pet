SELECT "shopapp_product"."id",
       "shopapp_product"."name",
       "shopapp_product"."description",
       "shopapp_product"."price",
       "shopapp_product"."created_at",
       "shopapp_product"."archived",
       "shopapp_product"."preview"
FROM "shopapp_product"
WHERE NOT "shopapp_product"."archived"
LIMIT 3;

--
SELECT "shopapp_product"."id",
       "shopapp_product"."name",
       "shopapp_product"."description",
       "shopapp_product"."price",
       "shopapp_product"."created_at",
       "shopapp_product"."archived",
       "shopapp_product"."preview"
FROM "shopapp_product"
WHERE "shopapp_product"."id" = 1
LIMIT 21;

SELECT "shopapp_productimage"."id",
       "shopapp_productimage"."product_id",
       "shopapp_productimage"."image"
FROM "shopapp_productimage"
WHERE "shopapp_productimage"."product_id" = 1;

--
--
