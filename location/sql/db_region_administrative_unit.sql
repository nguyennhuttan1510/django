-- Persist the region & administrative records, since this data does not comes from DVHCVN API

-- DATA for administrative_regions
INSERT INTO location_administrativeregion ("name",name_en,code_name,code_name_en) VALUES
	 ('Đông Bắc Bộ','Northeast','dong_bac_bo','northest'),
	 ('Tây Bắc Bộ','Northwest','tay_bac_bo','northwest'),
	 ('Đồng bằng sông Hồng','Red River Delta','dong_bang_song_hong','red_river_delta'),
	 ('Bắc Trung Bộ','North Central Coast','bac_trung_bo','north_central_coast'),
	 ('Duyên hải Nam Trung Bộ','South Central Coast','duyen_hai_nam_trung_bo','south_central_coast'),
	 ('Tây Nguyên','Central Highlands','tay_nguyen','central_highlands'),
	 ('Đông Nam Bộ','Southeast','dong_nam_bo','southeast'),
	 ('Đồng bằng sông Cửu Long','Mekong River Delta','dong_bang_song_cuu_long','southwest');

-- DATA for administrative_units
INSERT INTO location_administrativeunit (full_name,full_name_en,short_name,short_name_en,code_name,code_name_en) VALUES
	 ('Thành phố trực thuộc trung ương','Municipality','Thành phố','City','thanh_pho_truc_thuoc_trung_uong','municipality'),
	 ('Tỉnh','Province','Tỉnh','Province','tinh','province'),
	 ('Thành phố thuộc thành phố trực thuộc trung ương','Municipal city','Thành phố','City','thanh_pho_thuoc_thanh_pho_truc_thuoc_trung_uong','municipal_city'),
	 ('Thành phố thuộc tỉnh','Provincial city','Thành phố','City','thanh_pho_thuoc_tinh','provincial_city'),
	 ('Quận','Urban district','Quận','District','quan','urban_district'),
	 ('Thị xã','District-level town','Thị xã','Town','thi_xa','district_level_town'),
	 ('Huyện','District','Huyện','District','huyen','district'),
	 ('Phường','Ward','Phường','Ward','phuong','ward'),
	 ('Thị trấn','Commune-level town','Thị trấn','Township','thi_tran','commune_level_town'),
	 ('Xã','Commune','Xã','Commune','xa','commune');