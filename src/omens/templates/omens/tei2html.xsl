<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">
  <xsl:param name="omen">

    <!-- Content:template -->

  </xsl:param>

  <xsl:key name="witness" match="tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w/app/rdg" use="./@wit" />
  <xsl:template match="/">
    <div class="container">
      <h2 class="bd-title mt-3 mb-0">
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
          <a class="btn btn-light" role="button" href="tei.xml" target="BLANK">&#11123;
          </a>
        </small>
      </h2>

      <div id ="omens">
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
      </div>
    </div>
  </xsl:template>

  <xsl:template match="tei:body/tei:div"> <!-- Omen -->
    <div class="card">
      <xsl:choose>
        <xsl:when test="not($omen)"> <!-- parameter has not been supplied -->
          <div class="card-header">
            <xsl:value-of select="./@n"/>          <a  target="_blank" class="btn-sm btn-link text-decoration-none">
            <xsl:attribute name="href">/omens/<xsl:value-of select="@xml:id"/>/tei</xsl:attribute>
            &#8599;
          </a>
          </div>
        </xsl:when>
      </xsl:choose>

      <div class="card-body">
        <div  class="table-responsive">
          <table class="table-bordered table-striped table-condensed"><tbody>
            <xsl:apply-templates select="./div[@type = &apos;score&apos;]"/> <!-- Score -->
            <xsl:apply-templates select="./div[@n]"/> <!-- Reconstruction -->
          </tbody></table>
        </div>
        <xsl:apply-templates select="./div[@type = &apos;commentary&apos;]"/> <!-- Commentary -->
      </div>
    </div>
  </xsl:template>
  <xsl:template match="tei:body/tei:div/div[@type = &apos;score&apos;]"> <!-- Score -->
    <xsl:variable name="omenid" select="../@xml:id"/>
    <tr>
      <th colspan="100%">
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
            <!--  -->

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
      <th colspan="100%">
        <a data-toggle="collapse" role="button" aria-expanded="false" >
          <xsl:attribute name="href">#<xsl:value-of select="@xml:id"/>-reading</xsl:attribute>
          <xsl:value-of select="@n"/>
        </a>
      </th>
    </tr>
    <xsl:apply-templates select="./ab[@type = &apos;transliteration&apos;]"/>
    <xsl:apply-templates select="./ab[@type = &apos;transcription&apos;]"/>
    <xsl:apply-templates select="./ab[@type = &apos;translation&apos;]"/>
  </xsl:template>


  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]">
    <tr>
      <th scope="row">Translation (<xsl:value-of select="@lang"/>)</th>
      <td colspan="100%">
        <xsl:attribute name="lang">
          <xsl:value-of select="@lang"/>
        </xsl:attribute>
        <xsl:apply-templates select="./div[@type = &apos;protasis&apos;]"/>
        <xsl:apply-templates select="./div[@type = &apos;apodosis&apos;]"/>
      </td>
    </tr>
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
    <tr>
      <th scope="row">Transliteration</th>
      <xsl:for-each select="../../div[@type = &apos;score&apos;]/ab/w">
        <xsl:sort select="./@xml:id"/>
        <!-- <xsl:for-each select="//tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w"> -->
        <xsl:variable name="wordid" select="./@xml:id"/>
        <td>
          <xsl:value-of select="../../../div[@n=$rdgid]/ab[@type = &apos;transliteration&apos;]/w[@corresp=$wordid]"/>
        </td>
      </xsl:for-each>
    </tr>
  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;transcription&apos;]">
    <xsl:variable name="rdgid" select="../@n"/>
    <tr>
      <th scope="row">Transcription</th>
      <xsl:for-each select="../../div[@type = &apos;score&apos;]/ab/w">
        <xsl:sort select="./@xml:id"/>
        <!-- <xsl:for-each select="//tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w"> -->
        <xsl:variable name="wordid" select="./@xml:id"/>
        <td>
          <xsl:value-of select="../../../div[@n=$rdgid]/ab[@type = &apos;transcription&apos;]/w[@corresp=$wordid]"/>
        </td>
      </xsl:for-each>
    </tr>
  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@type = &apos;commentary&apos;]"> <!-- Commentary -->
    <a data-toggle="collapse" role="button" aria-expanded="false" >
      <xsl:attribute name="href">#<xsl:value-of select="../@xml:id"/>-comments</xsl:attribute>
      <small class="text-muted"><xsl:value-of select="./head"/></small>
    </a>
    <div class="collapse">
      <xsl:attribute name="id"><xsl:value-of select="../@xml:id"/>-comments</xsl:attribute>
      <xsl:for-each select="./p">
        <p><xsl:value-of select ="."/></p>
      </xsl:for-each>
    </div>
  </xsl:template>

</xsl:stylesheet>
