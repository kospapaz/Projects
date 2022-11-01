install.packages("RSQLite")
install.packages("tidyverse")
library(DBI)
library(dplyr)

# Σύνδεση στο πακέτο μας#

con <- dbConnect(RSQLite::SQLite(),"D:\\Σχολή\\ANALUSH\\ERGASIA ANALUSH\\archive\\database.sqlite")
con

# Εμφάνιση, Ανάγνωση και εμφάνιση δομής όλων των tables"

dbListTables(con)

dbReadTable(con,"Country")

dbReadTable(con,"League")

dbReadTable(con,"Match")

dbReadTable(con,"Player")

dbReadTable(con,"Player_Attributes")

dbReadTable(con,"Team")

dbReadTable(con,"Team_Attributes")

dbReadTable(con,"sqlite_sequence")

str(dbReadTable(con,"Country"))

str(dbReadTable(con,"League"))

str(dbReadTable(con,"Match"))

str(dbReadTable(con,"Player"))

str(dbReadTable(con,"Player_Attributes"))

str(dbReadTable(con,"Team"))

str(dbReadTable(con,"Team_Attributes"))

str(dbReadTable(con,"sqlite_sequence"))

# Χρήση tbl() για παραγωγή pointer και εξέταση των διαστάσεων του καθενός#

country<- tbl(con,"Country")

league<- tbl(con,"League")

match<-tbl(con,"Match")

player <- tbl(con,"Player")

playerattributes <- tbl(con,"Player_Attributes")

team <- tbl(con,"Team")

teamattributes <- tbl(con, "Team_Attributes")

dim(country)

dim(league)

dim(match)

dim(player)

dim(playerattributes)

dim(team)

dim(teamattributes)


# Ερωτήματα της προηγούμενης άσκησης μόνο με χρήση dplyr#

# Εμφάνιση ονόματος των παικτών, ταξινομημένη φθίνουσα κατά βάρος και φιλτραρισμένη κατά ύψος  #

a<-(select(player,player_name,height,weight))%>%
  
      filter(height>=160 & height<=180)%>%
  
        arrange(-weight)

a


# Σύνδεση 2 tables και εμφάνιση αποτελεσμάτων για τη γηπεδούχο ομάδα #

b <- match %>%
  
      inner_join(team,by=c("home_team_api_id" = "team_api_id")) %>%
  
        filter(match_api_id==492473) %>%
  
          summarize(team_long_name,date,home_team_goal) 

b

# Σύνδεση και παρουσίαση των γηπεδούχων ομάδων με τη χώρα όπου εδρεύει # 

c <- team %>% 
  
       inner_join(match,by = c("team_api_id" = "home_team_api_id")) %>%
  
         inner_join(country, by = c("country_id"="id")) %>%
  
             distinct(name,team_long_name)

c

# Ερώτημα εμφάνιση του αποτελέσματος για τον αγώνα με id 492473 #
d <- match %>%
  
      filter(match_api_id == 492473) %>%
  
        left_join(team,by =c("home_team_api_id" = "team_api_id")) %>%
  
          left_join(team,by = c("away_team_api_id" = "team_api_id"), suffix=c(".Home" , ".Away")) %>%
  
            summarize(team_long_name.Home, team_long_name.Away, home_team_goal, away_team_goal)

d


# Εύρεση προτιμώμενου ποδιού παικτών και εκκαθάριση NAs #

prot_podi<- playerattributes %>%
  
                select(preferred_foot)%>% 
  
                   filter(preferred_foot=="right" || preferred_foot == "left") %>%
  
                     group_by(preferred_foot) %>%
  
                       summarize(count("left"))

prot_podi      

# Εκκαθάριση NAs #

df<-data.frame(playerattributes %>%
                 
                 select(preferred_foot))

summary(df)

sum(is.na(df))

cleardf<-na.omit(df)

summary(cleardf)


# Ραβδόγραμμα #

library(ggplot2)

# 1η περίπτωση με τα NAs #

ggplot(playerattributes,aes(preferred_foot)) +
  
        geom_bar() +  
  
          scale_y_continuous(labels=scales::comma)

# 2η περίπτωση μετά την αφαίρεση των NAs #

ggplot(cleardf,aes(preferred_foot)) +
  
          geom_bar() + 
  
            scale_y_continuous(labels=scales::comma)

# Διάγραμμα διασποράς #

ggplot(player,aes(x=height, y=weight)) +
          
         geom_point()

# Βελτιωμένο διάγραμμα διασποράς για την αποφυγή overplotting #

ggplot(player,aes(x=height, y=weight)) + 
      
        geom_jitter(alpha=0.5)

