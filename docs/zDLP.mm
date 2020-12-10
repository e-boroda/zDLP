<map version="freeplane 1.3.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="zDLP" ID="ID_1723255651" CREATED="1283093380553" MODIFIED="1607367242057"><hook NAME="MapStyle" zoom="1.5">
    <properties show_note_icons="true"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node">
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right">
<stylenode LOCALIZED_TEXT="default" MAX_WIDTH="600" COLOR="#000000" STYLE="as_parent">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.note"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="5"/>
<node TEXT="Objects" POSITION="right" ID="ID_1501205157" CREATED="1606974299000" MODIFIED="1607367229599" HGAP="26" VSHIFT="-42">
<edge COLOR="#ff0000"/>
<node TEXT="Storage" ID="ID_827362117" CREATED="1606974370400" MODIFIED="1607366521942">
<node TEXT="Files" ID="ID_158722882" CREATED="1606974456881" MODIFIED="1607368222275">
<icon BUILTIN="button_ok"/>
<icon BUILTIN="100%"/>
</node>
<node TEXT="Containers" ID="ID_1913261339" CREATED="1606974470877" MODIFIED="1607366548657">
<node TEXT="rar" ID="ID_1709438117" CREATED="1607020809260" MODIFIED="1607020818612"/>
<node TEXT="zip" ID="ID_1696448403" CREATED="1607020820225" MODIFIED="1607020823274"/>
<node TEXT="7z" ID="ID_681489506" CREATED="1607020824398" MODIFIED="1607020836562"/>
<node TEXT="iso" ID="ID_784937302" CREATED="1607020837474" MODIFIED="1607021178159"><richcontent TYPE="NOTE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      ISO images
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="Databases" ID="ID_248039453" CREATED="1606974480919" MODIFIED="1607366778920"/>
</node>
<node TEXT="Exchange" ID="ID_1936635828" CREATED="1606974417795" MODIFIED="1607366532198">
<icon BUILTIN="0%"/>
<node TEXT="MTA" ID="ID_333161078" CREATED="1606974766767" MODIFIED="1607366574269">
<node TEXT="MS Exchange" ID="ID_1880644892" CREATED="1606974773189" MODIFIED="1606974805993"/>
<node TEXT="Sendmail" ID="ID_1485815581" CREATED="1606974809281" MODIFIED="1606974817781"/>
<node TEXT="Postfix" ID="ID_1558014555" CREATED="1606974818755" MODIFIED="1606974823449"/>
</node>
<node TEXT="Removable media" ID="ID_1131891569" CREATED="1606974928408" MODIFIED="1607366595206" HGAP="15" VSHIFT="12"/>
</node>
</node>
<node TEXT="Functions" POSITION="right" ID="ID_1813092841" CREATED="1606974528778" MODIFIED="1607367226551" HGAP="44" VSHIFT="12">
<edge COLOR="#0000ff"/>
<node TEXT="Scan" ID="ID_699985084" CREATED="1606974538617" MODIFIED="1607366680772"/>
<node TEXT="Check" ID="ID_1831961350" CREATED="1606974550241" MODIFIED="1607366685803"/>
<node TEXT="Log" ID="ID_1149394165" CREATED="1606974556513" MODIFIED="1607367025723"/>
<node TEXT="Report" ID="ID_624988197" CREATED="1606974578191" MODIFIED="1607366699414"/>
<node TEXT="DB admin" ID="ID_748157319" CREATED="1607366716498" MODIFIED="1607366726573"/>
</node>
<node TEXT="Depends" POSITION="left" ID="ID_9431152" CREATED="1607003394648" MODIFIED="1607367233874" HGAP="50" VSHIFT="-26">
<edge COLOR="#00ff00"/>
<node TEXT="Python libs" ID="ID_1167126593" CREATED="1607003421290" MODIFIED="1607367138345" HGAP="24" VSHIFT="-25">
<node TEXT="textract" ID="ID_538524615" CREATED="1607003526990" MODIFIED="1607366163100">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_289638339" STARTINCLINATION="104;-5;" ENDINCLINATION="104;-5;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_883601168" STARTINCLINATION="76;-4;" ENDINCLINATION="76;-4;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_728930337" STARTINCLINATION="69;9;" ENDINCLINATION="69;9;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_1509116102" STARTINCLINATION="23;0;" ENDINCLINATION="47;4;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<node TEXT="bugs" ID="ID_1868091994" CREATED="1607364400484" MODIFIED="1607364405921">
<node TEXT="ShellParser Patch" ID="ID_1579289086" CREATED="1607364410912" MODIFIED="1607364421242"/>
</node>
</node>
<node TEXT="pdfminer.six" ID="ID_723851928" CREATED="1607003902963" MODIFIED="1607366182042" HGAP="26" VSHIFT="10"/>
<node TEXT="unrar" ID="ID_1105668032" CREATED="1607363630050" MODIFIED="1607367138344" VSHIFT="12">
<node TEXT="bug" ID="ID_106651548" CREATED="1607363713373" MODIFIED="1607365846439">
<node TEXT="date-time" ID="ID_857099474" CREATED="1607364334127" MODIFIED="1607364341709"/>
</node>
</node>
</node>
<node TEXT="Software" ID="ID_57231367" CREATED="1607003453725" MODIFIED="1607366170440" HGAP="26" VSHIFT="48">
<node TEXT="poppler" ID="ID_1509116102" CREATED="1607003480940" MODIFIED="1607366170438" HGAP="14" VSHIFT="-6"/>
<node TEXT="unrtf" ID="ID_728930337" CREATED="1607003588201" MODIFIED="1607003593095"/>
<node TEXT="antiword" ID="ID_883601168" CREATED="1607003552417" MODIFIED="1607003869906">
<node TEXT="feature" ID="ID_319691257" CREATED="1607365812451" MODIFIED="1607365840423">
<node TEXT="set HOME on Win" ID="ID_154748393" CREATED="1607365865594" MODIFIED="1607366044792"><richcontent TYPE="DETAILS" HIDDEN="true">

<html>
  <head>
    
  </head>
  <body>
    <p>
      Differences between the Unix version of Antiword and the Windows version
    </p>
    <p>
      =================================================
    </p>
    <p>
      
    </p>
    <p>
      (1)
    </p>
    <p>
      The Unix version looks for its mapping files in $HOME/.antiword.
    </p>
    <p>
      The Windows version looks for its mapping files in %HOME%\antiword if HOME is set
    </p>
    <p>
      and in C:\antiword if HOME is not set.
    </p>
    <p>
      
    </p>
    <p>
      (2)
    </p>
    <p>
      The Antiword executable (antiword.exe) can be placed in any directory. If you
    </p>
    <p>
      choose a directory from your %PATH%, you will not have to use a full pathname
    </p>
    <p>
      every time.
    </p>
  </body>
</html>

</richcontent>
</node>
</node>
</node>
<node TEXT="tesseract" ID="ID_289638339" CREATED="1607003594258" MODIFIED="1607003641979"/>
<node TEXT="UnRAR.dll" ID="ID_829497990" CREATED="1607367097184" MODIFIED="1607367108171"/>
</node>
</node>
<node TEXT="DB" POSITION="left" ID="ID_1058607902" CREATED="1607020552616" MODIFIED="1607367236686" HGAP="77" VSHIFT="-36">
<edge COLOR="#ff00ff"/>
<node TEXT="Tables" ID="ID_835053167" CREATED="1607020579451" MODIFIED="1607366663637">
<node TEXT="obj" ID="ID_1628978735" CREATED="1607020592527" MODIFIED="1607020603581"/>
<node TEXT="root" ID="ID_1110722877" CREATED="1607020605941" MODIFIED="1607020609469">
<node TEXT="protocol" ID="ID_1668262086" CREATED="1607020688971" MODIFIED="1607020695876"/>
<node TEXT="host" ID="ID_895545492" CREATED="1607020697104" MODIFIED="1607020710545"/>
<node TEXT="root" ID="ID_1764986768" CREATED="1607020700131" MODIFIED="1607020719100"/>
<node TEXT="description" ID="ID_68777151" CREATED="1607020720034" MODIFIED="1607020725253"/>
</node>
</node>
</node>
<node TEXT="Roadmap" POSITION="left" ID="ID_840497701" CREATED="1607363660692" MODIFIED="1607367242056" HGAP="56" VSHIFT="14">
<edge COLOR="#00ffff"/>
</node>
</node>
</map>
