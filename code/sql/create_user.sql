do
$$
begin
  if not exists (select * from pg_roles where rolname = 'analyst') then
     create role analyst NOLOGIN; 
  end if;
  if not exists (select * from pg_user where usename = 'analyst_team') then
     create user analyst_team password '12345';
      GRANT CONNECT on DATABASE homex to analyst_team;
	  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO analyst_team;
  end if;
end
$$
;
