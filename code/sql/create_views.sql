do
$$
begin
  if not exists (SELECT * FROM
        information_schema.tables
    WHERE
        table_schema = 'public' AND
		table_type = 'VIEW' and
        table_name  = 'country_info')
	then
		CREATE VIEW  country_info as
			select wc.id, wc."iso2Code", wc.name, rc."name.common", rc."name.official",
				rc."unMember", rc."altSpellings", rc.landlocked, rc.population, rc.timezones,
				rc."car.side", rc."flags.png", rc."flags.svg",
				wc.longitude, wc.latitude, wc."region.id", wc."region.iso2code", wc."region.value",
				rc.region, rc.continents, rc."maps.googleMaps", rc."maps.openStreetMaps",
				wc."incomeLevel.id", wc."incomeLevel.iso2code", wc."incomeLevel.value",
				wc."lendingType.id", wc."lendingType.iso2code", wc."lendingType.value",
				rc."startOfWeek"
			from world_country wc, rest_country rc
			where wc."iso2Code" = rc.cca2 and wc.id = rc.cca3  ;
  end if;
end
$$
;
