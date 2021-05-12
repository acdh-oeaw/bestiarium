<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">
  <xsl:param name="omen">

    <!-- Content:template -->

  </xsl:param>

  <xsl:key name="witness" match="tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w/app/rdg" use="./@wit" />
  <xsl:template match="/">
    <div class="container">
      <h5 class="bd-title mt-3 mb-0">
        <!-- parameter has not been supplied -->
        <xsl:choose>
          <xsl:when test="$omen">
            Omen <xsl:value-of select=".//tei:body/tei:div[@xml:id = $omen]/@n"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select=".//tei:title"/>
          </xsl:otherwise>
        </xsl:choose>
        <small>
          <a class="btn btn-light" role="button" href="../tei.xml" target="BLANK">&#11123;
          </a>
        </small>
        <div class="intro">Some introductory text about this chapter. Suggestions: Which animal this is about, how many omens are in it - and how many tablets are found to contain omens from this chapter? Is there a theme?
        <div>
          <a class="btn btn-light btn-sm" type="button" href="#">K-02925-</a>
          <a class="btn btn-light btn-sm" href="#">VAT-10523_2</a>
        </div>
        </div>
        <div class="toggle-buttons">
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="Transliteration" checked="true"
                 onclick="toggleClass(this, 'transliteration')"/>
          <label class="form-check-label" for="inlineCheckbox1"><small class="text-muted">Transliteration</small></label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value="Transcription" checked="true"
                 onclick="toggleClass(this, 'transcription')"/>
          <label class="form-check-label" for="inlineCheckbox1"><small class="text-muted">Transcription</small></label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="inlineCheckbox2" value="Translation" checked="true"
                 onclick="toggleClass(this, 'translation')"/>
          <label class="form-check-label" for="inlineCheckbox1"><small class="text-muted">Translation</small></label>
        </div>
        </div>
      </h5>

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
    <tr><td colspan="100%">
      <table class="table-condensed score-table">
        <xsl:apply-templates select="./div[@type = &apos;score&apos;]"/> <!-- Score -->
      </table>
    </td>
    </tr>
    <xsl:apply-templates select="./div[@n]"/> <!-- Reconstruction -->

  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@type = &apos;score&apos;]"> <!-- Score -->
    <xsl:variable name="omenid" select="../@xml:id"/>
    <tr>
      <th colspan="100%">
        <xsl:value-of select="substring-after($omenid, 'Omen-')"/>&#160;
        <a data-toggle="collapse" role="button" aria-expanded="false"  >
          <xsl:attribute name="data-target">.<xsl:value-of select="$omenid"/>-score-row</xsl:attribute>
          <xsl:attribute name="href">#<xsl:value-of select="$omenid"/>-score</xsl:attribute>
          <small>Score</small>
        </a>
      </th>
    </tr>
    <xsl:for-each select="../../../../tei:teiHeader/tei:sourceDesc/tei:listWit/tei:witness">
      <xsl:variable name="witid" select="@xml:id"/>
      <xsl:if test="../../../../tei:text/tei:body/tei:div[@xml:id=$omenid]/div/ab/w/app/rdg[@wit=$witid]">
        <!-- if witness is used in the score -->
        <tr>
          <xsl:attribute name="class">small <xsl:value-of select="$omenid"/>-score-row collapse</xsl:attribute>
          <td >
            <xsl:value-of select="./tei:idno"/>
          </td>
          <xsl:for-each
              select="../../../../tei:text/tei:body/tei:div[@xml:id=$omenid]/div[@type = &apos;score&apos;]/ab/w">
            <xsl:sort select="./@xml:id"/>
            <td>
              <xsl:value-of select="app/rdg[@wit=$witid]" />
            </td>
          </xsl:for-each>
        </tr>
      </xsl:if>
    </xsl:for-each>

  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w"> <!-- Words in the score -->
    <th scope="col"><small><xsl:value-of select="@xml:id"/></small></th>
  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@n]"> <!-- Reconstruction -->
    <tr>
      <td class="reconstruction-label">
        <small><xsl:value-of select="@n"/></small>
      </td>

      <xsl:apply-templates select="./ab[@type = &apos;transliteration&apos;][1]"/>
      <xsl:apply-templates select="./ab[@type = &apos;transcription&apos;][1]"/>
      <xsl:apply-templates select="./ab[@type = &apos;translation&apos;][1]"/>
    </tr>
  </xsl:template>


  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]">
    <!-- <th scope="row">Translation (<xsl:value-of select="@lang"/>)</th> -->
    <td class="translation">
      <xsl:attribute name="lang">
        <xsl:value-of select="@lang"/>
      </xsl:attribute>
      <xsl:apply-templates select="./div[@type = &apos;protasis&apos;]"/>–
      <xsl:apply-templates select="./div[@type = &apos;apodosis&apos;]"/>
    </td>
  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]/div[@type = &apos;protasis&apos;]">
    <span class="protasis">
      <xsl:value-of select="." />
    </span>
  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]/div[@type = &apos;apodosis&apos;]">
    <span class="apodosis">
      <xsl:value-of select="." />
    </span>
  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;transliteration&apos;]">
    <xsl:variable name="rdgid" select="../@n"/>
    <!-- <xsl:value-of select="@xml:id"/> -->
    <!-- <th scope="row">Transliteration</th> -->
    <td class="transliteration">
      <xsl:for-each select="../../div[@type = &apos;score&apos;]/ab/w">
        <xsl:sort select="./@xml:id"/>
        <!-- <xsl:for-each select="//tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w"> -->
        <xsl:variable name="wordid" select="./@xml:id"/>
        <span class="lemma"><xsl:value-of select="../../../div[@n=$rdgid]/ab[@type = &apos;transliteration&apos;]/w[@corresp=$wordid]"/></span>
      </xsl:for-each>
    </td>

  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;transcription&apos;]">
    <xsl:variable name="rdgid" select="../@n"/>
    <!-- <th scope="row">Transcription</th> -->
    <td class="transcription">
      <xsl:for-each select="../../div[@type = &apos;score&apos;]/ab/w">
        <xsl:sort select="./@xml:id"/>
        <xsl:variable name="wordid" select="./@xml:id"/>
        <span class="lemma"><xsl:value-of select="../../../div[@n=$rdgid]/ab[@type = &apos;transcription&apos;]/w[@corresp=$wordid]"/></span>
        </xsl:for-each>
    </td>
  </xsl:template>
</xsl:stylesheet>
