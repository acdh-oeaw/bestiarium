<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">
  <xsl:param name="omen">

    <!-- Content:template -->

  </xsl:param>

  <xsl:key name="witness" match="tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w/app/rdg" use="./@wit" />
  <xsl:template match="/">
    <div id ="omens">
      <div  class="table-responsive">
        <table class="table-striped table-condensed"><tbody>
          <xsl:choose>
            <xsl:when test="not($omen)"> <!-- parameter has not been supplied -->
              <xsl:apply-templates select=".//tei:body/tei:div"> <!-- All Omens -->
                <xsl:sort select="./@n" data-type="number"/>
              </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise> <!--parameter has been supplied -->
              <xsl:apply-templates select=".//tei:body/tei:div[@xml:id = $omen]"/> <!-- Omen -->
            </xsl:otherwise>
          </xsl:choose>
        </tbody></table>
      </div>
    </div>
  </xsl:template>

  <xsl:template match="tei:body/tei:div"> <!-- Omen -->

    <!-- <xsl:choose> -->
    <!--   <xsl:when test="not($omen)"> <!-\- parameter has not been supplied -\-> -->
    <!--     <div class="card-header"> -->
    <!--       <xsl:value-of select="./@n"/> -->
    <!--       <a  target="_blank" class="btn-sm btn-link text-decoration-none"> -->
    <!--         <xsl:attribute name="href">/omens/<xsl:value-of select="@xml:id"/>/tei</xsl:attribute> -->
    <!--         &#8599; -->
    <!--       </a> -->
    <!--     </div> -->
    <!--   </xsl:when> -->
    <!-- </xsl:choose> -->

    <xsl:apply-templates select="./div[@type = &apos;score&apos;]"/> <!-- Score -->
    <xsl:apply-templates select="./div[@n]"/> <!-- Reconstruction -->

  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@type = &apos;score&apos;]"> <!-- Score -->
    <xsl:variable name="omenid" select="../@xml:id"/>
    <tr>
      <th colspan="100%">
        <xsl:choose>
          <xsl:when test="not($omen)"> <!-- parameter has not been supplied -->
            <a  target="_blank" class="btn-sm btn-link text-decoration-none">
              <xsl:attribute name="href">/omens/<xsl:value-of select="$omenid"/>/tei</xsl:attribute>
              &#8599;
            </a>
          </xsl:when>
        </xsl:choose>
        <xsl:value-of select="substring-after($omenid, 'Omen-')"/>&#160;
        <a data-toggle="collapse" role="button" aria-expanded="false"  >
          <xsl:attribute name="data-target">.<xsl:value-of select="$omenid"/>-score-row</xsl:attribute>
          <xsl:attribute name="href">#<xsl:value-of select="$omenid"/>-score</xsl:attribute>
          <small>Score</small>
        </a>
      </th>
    </tr>
    <tr>
      <xsl:attribute name="class">small <xsl:value-of select="$omenid"/>-score-row collapse</xsl:attribute>
      <td colspan="100%">
        <table class="table-condensed score-table">
          <xsl:for-each select="../../../../tei:teiHeader/tei:sourceDesc/tei:listWit/tei:witness">
            <xsl:variable name="witid" select="@xml:id"/>
            <xsl:if test="../../../../tei:text/tei:body/tei:div[@xml:id=$omenid]/div/ab/w/app/rdg[@wit=$witid]">
              <!-- if witness is used in the score -->
              <tr>
                <td >
                  <xsl:value-of select="./tei:idno"/>
                </td>
                <xsl:for-each
                    select="../../../../tei:text/tei:body/tei:div[@xml:id=$omenid]/div[@type = &apos;score&apos;]/ab/w">
                  <xsl:sort select="./@xml:id"/>
                  <td>
                      <xsl:apply-templates select="app/rdg[@wit=$witid]"/>
                  </td>
                </xsl:for-each>
              </tr>
            </xsl:if>
          </xsl:for-each>
        </table>
      </td>
    </tr>
  </xsl:template>
 
  <xsl:template match="anchor">
   <xsl:choose>
      <xsl:when test="@type='breakStart'"> 
        <xsl:text>[</xsl:text>
      </xsl:when>
      <xsl:when test="@type='breakEnd'"> 
        <xsl:if test="../damageSpan"><xsl:text>&#11811;</xsl:text></xsl:if>
        <xsl:if test="not(../damageSpan)"><xsl:text>]</xsl:text></xsl:if>
      </xsl:when>
    </xsl:choose>
   </xsl:template>

  <xsl:template match="damageSpan">
      <xsl:text>&#11810;</xsl:text>
  </xsl:template>


  <xsl:template match="tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w"> <!-- Words in the score -->
    <th scope="col"><small><xsl:value-of select="@xml:id"/></small></th>
  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@n]"> <!-- Reconstruction -->
    <tr>
      <td class="reconstruction-label">
        <xsl:value-of select="@n"/>
        <xsl:if test="*[@source]">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" value="others">
              <xsl:attribute name="id">
                <xsl:value-of select="./@xml:id"/>-others
              </xsl:attribute>
              <xsl:attribute name="onclick">
                toggleClass&#x28;this,&apos;<xsl:value-of select="./@xml:id"/>-others&apos;&#x29;
              </xsl:attribute>
            </input>
            <label class="form-check-label" >
              <xsl:attribute name="for">
                <xsl:value-of select="./@xml:id"/>-others
              </xsl:attribute>
              <small class="text-muted">Previous readings and translations</small>
            </label>
          </div>
        </xsl:if>


      </td>
      <td class="transliteration"><ul class="list-group">
        <xsl:apply-templates select="./ab[@type = &apos;transliteration&apos;]"/></ul>
      </td>
      <td class="transcription"><ul class="list-group">
        <xsl:apply-templates select="./ab[@type = &apos;transcription&apos;]"/>
      </ul>
      </td>
      <td class="translation"><ul class="list-group">
        <xsl:apply-templates select="./ab[@type = &apos;translation&apos;]"/>
      </ul>
      </td>
    </tr>
  </xsl:template>


  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]">
    <!-- <th scope="row">Translation (<xsl:value-of select="@lang"/>)</th> -->
    <li class="list-group-item">
      <xsl:attribute name="lang">
        <xsl:value-of select="@lang"/>
      </xsl:attribute>
      <xsl:choose>
        <xsl:when test="@source">
          <xsl:attribute name="class">list-group-item <xsl:value-of select="../@xml:id"/>-others others d-none </xsl:attribute>
          <xsl:value-of select="@source"/>
        </xsl:when>
      </xsl:choose>
      <div>
        <xsl:attribute name="id"><xsl:value-of select="./@xml:id"/>
        </xsl:attribute>
        <xsl:apply-templates select="./div[@type = &apos;protasis&apos;]"/>
        <xsl:apply-templates select="./div[@type = &apos;apodosis&apos;]"/>
      </div>
    </li>
  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]/div[@type = &apos;protasis&apos;]">
    <span class="protasis">
      <xsl:value-of select="." />
    </span>
  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]/div[@type = &apos;apodosis&apos;]">
    <xsl:if test=".!=''">
      &#x2D;&#160;
    <span class="apodosis">
      <xsl:value-of select="." />
    </span>
    </xsl:if>
  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;transliteration&apos;]">
    <xsl:variable name="rdgid" select="../@n"/>
    <xsl:variable name="rdgxmlid" select="@xml:id"/>
    <!-- <xsl:value-of select="@xml:id"/> -->
    <!-- <th scope="row">Transliteration</th> -->
    <li  class="list-group-item">
      <xsl:choose>
        <xsl:when test="@source">
          <xsl:attribute name="class">list-group-item <xsl:value-of select="../@xml:id"/>-others others d-none</xsl:attribute>
          <xsl:value-of select="@source"/>
        </xsl:when>
      </xsl:choose>
      <div>
        <xsl:attribute name="id"><xsl:value-of select="./@xml:id"/>
        </xsl:attribute>
        <xsl:for-each select="../../div[@type = &apos;score&apos;]/ab/w">
          <xsl:sort select="./@xml:id"/>
          <!-- <xsl:for-each select="//tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w"> -->
          <xsl:variable name="wordid" select="./@xml:id"/>
          <span class="lemma">
            <xsl:apply-templates select="../../../div[@n=$rdgid]/ab[@xml:id = $rdgxmlid]/w[@corresp=$wordid]"/>
            </span>
        </xsl:for-each>
      </div>
    </li>
  </xsl:template>


  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;transcription&apos;]">
    <xsl:variable name="rdgid" select="../@n"/>
    <xsl:variable name="rdgxmlid" select="@xml:id"/>
    <!-- <th scope="row">Transcription</th> -->
    <li  class="list-group-item">
      <xsl:choose>
        <xsl:when test="@source">
          <xsl:attribute name="class">list-group-item <xsl:value-of select="../@xml:id"/>-others others d-none</xsl:attribute>
          <xsl:value-of select="@source"/>
        </xsl:when>
      </xsl:choose>
      <div>
        <xsl:attribute name="id"><xsl:value-of select="./@xml:id"/>
        </xsl:attribute>
        <xsl:for-each select="../../div[@type = &apos;score&apos;]/ab/w">
          <xsl:sort select="./@xml:id"/>
          <xsl:variable name="wordid" select="./@xml:id"/>
          <span class="lemma">
            <xsl:apply-templates select="../../../div[@n=$rdgid]/ab[@xml:id = $rdgxmlid]/w[@corresp=$wordid]"/>
          </span>
        </xsl:for-each>
      </div>
    </li>
  </xsl:template>

</xsl:stylesheet>
