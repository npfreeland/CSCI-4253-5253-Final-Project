


i = PlayerCareerStats(player_id="203999").season_totals_regular_season.get_data_frame()
i = i[i["SEASON_ID"]=="2022-23"]
print(i)
li = []
print(li.append(i.to_dict(orient = 'list')))
l = PlayerCareerStats(player_id="203999").season_totals_regular_season.get_data_frame()
l = l[l["SEASON_ID"]=="2021-22"]
print(l)
print(li.append(l.to_dict(orient = 'list')))
print("combine list")
print(li)