Copy (
Select ps.mainarea_id,ps.secondarea_id,ps.embadon,ps.longitude,ps.latitude,ps.asset_type_id,ps.bedrooms,ps.construction_year,tc.source_id,tc.selling_price
from tran_commercial as tc, prop_residential as ps where tc.asset_id=ps.id and ps.construction_year ~ '^\d+$'
) To '/Users/konstantinosskianis/Desktop/test.csv' With CSV DELIMITER ',' HEADER;
