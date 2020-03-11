select Article_Search_Keywords from /*[Tosearch_Keyword]*/
(
	select a.ToSearch_Keyword_ID, IF(RIGHT(a.Keyword,1)='@',SUBSTRING_INDEX(a.Keyword,'@',1),a.Keyword) as Article_Search_Keywords,a.A,a.Keyword, a.Client_ID,a.Is_Active,a.Subject_ID,a.Is_For_Website_Inner,a.Is_For_Search_Engine,a.Is_For_Oversea_Website,a.Priority_Level,a.Created_Time,b.Website_Search_Type,
        if(a.Created_Time BETWEEN DATE_SUB(NOW(),INTERVAL 12 HOUR) and NOW(),1,0) as Lastest_Word,b.Website_Purpose_Type,a.Last_Update_time
	from
	(
	  SELECT t.*,'' as Website_No from tosearch_keyword_no_website_group t where (t.Expire_Time>=NOW() or t.Expire_Time is null)
				and (if('1'+1=1,1,0)=1 or (Last_Update_time BETWEEN DATE_SUB(NOW(),INTERVAL 10 MINUTE) and NOW()))
				and (if('0'+1=1,1,0)=1 or Need_Extra_Schedule=if('0'+0=0,0,'0'+0))
	  union
	  SELECT * from tosearch_keyword_with_group where Website_No='S0038' and (Expire_Time>=NOW() or Expire_Time is null)
				and (if('1'+1=1,1,0)=1 or (Last_Update_time BETWEEN DATE_SUB(NOW(),INTERVAL 10 MINUTE) and NOW()))
				and (if('0'+1=1,1,0)=1 or Need_Extra_Schedule=if('0'+0=0,0,'0'+0))
    ) a JOIN website b
	on 1=1 and b.Website_No='S0038' and (ABS(a.ToSearch_Keyword_ID) mod 1=0)
	and Subject_ID in(SELECT Subject_ID from `subject` where if('0'+1=1,1,0)=1 or Priority_Level=if('0'+0=0,0,'0'+0))
	and (if('0'+1=1,1,0)=1 or a.Client_ID=if('0'+0=0,0,'0'+0))
    and a.Client_ID in(SELECT Client_ID from `client` where if(''+1=1,1,0)=1 or Priority_Level=if(''+0=0,0,''+0))
	and a.Client_ID in(SELECT Client_ID from `client` where 1=1 AND (IF(CONCAT('','N')='N',1,0)=1  OR Is_Trial_Client=IF(CONCAT('','N')='N','0','')))
	and (if('0'+1=1,1,0)=1 or a.Subject_ID=if('0'+0=0,0,'0'+0))
	and (if(''+1=1,1,0)=1 or a.ToSearch_Keyword_ID=if(''+0=0,0,''+0))
        and (if('0'+0=1,1,0)=1 or (Subject_ID in (SELECT subject_id from `subject`)))
	where (a.Is_For_Website_Inner=1 and b.Website_Search_Type='I')
	or (a.Is_For_Search_Engine=1 and b.Website_Search_Type='S')
	or (a.Is_For_Oversea_Website=1 and b.Website_Search_Type='O')
) Search_Keyword
left join
(select b.Website_Main_Page_URL as ListPage_URL,b.Website_No,b.Default_Save_Rule as ListPage_Save_Rule,b.LinkURL_Include_Keywords_CommaText,b.LinkURL_Exclude_Keywords_CommaText,
b.LinkURL_Min_Length,b.LinkText_Include_Keywords_CommaText,b.LinkText_Exclude_Keywords_CommaText,b.LinkText_Min_Length,
b.Media_Type_Code,b.Website_Column_Level,b.Website_Important_Level,b.Login_Account,b.Login_Password,b.Set_Article_Section_ID,b.Website_Language_Code,if(b.Website_Language_Code in('CN','TW','JA','KO'),1,0) as Website_Is_Chinese
from website b
where b.Website_No='S0038') Website_Info on 1=1
group by keyword
ORDER BY Lastest_Word desc,Search_Keyword.Priority_Level desc,Search_Keyword.Last_Update_time desc,Search_Keyword.ToSearch_Keyword_ID desc
limit 10