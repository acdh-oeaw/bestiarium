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
          <a class="btn btn-light" role="button" >
            <xsl:attribute name="href">tei</xsl:attribute>
            TEI
          </a>
        </small>

        <small>
          <a class="btn btn-light" role="button" target="BLANK">
            <xsl:attribute name="href">tei.xml</xsl:attribute>
            &#11123;
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
            <h5><xsl:value-of select="./@n"/>          <a  target="_blank" class="btn-sm btn-link text-decoration-none">
            <xsl:attribute name="href">/omens/<xsl:value-of select="@xml:id"/>/tei</xsl:attribute>
            &#8599;
          </a>
            </h5>
          </div>
        </xsl:when>
      </xsl:choose>

      <div class="card-body">
            <ul class="list-group list-group-flush">
              <xsl:apply-templates select="./div[@n]"/> <!-- Reconstruction -->
            </ul>
      </div>
    </div>
  </xsl:template>

  <xsl:template match="tei:body/tei:div/div[@n]"> <!-- Reconstruction -->
        <xsl:variable name="rdgname" select="@n"/>

      <li class="list-group-item m-0 p-1 border-0">
      <h6 class="card-title mb-0 mt-1">
          <xsl:value-of select="@n"/>
      </h6>
      </li>
      <li class="list-group-item border-0 p-1" >
      <ul class="list-group list-group-flush">

    <xsl:apply-templates select="./ab[@type = &apos;transcription&apos;]"/>
    <xsl:apply-templates select="./ab[@type = &apos;translation&apos;]"/>
      </ul>
      </li>

  </xsl:template>


  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;translation&apos;]">
<li class="list-group-item border-0 p-1" >
        <xsl:attribute name="lang">
          <xsl:value-of select="@lang"/>
        </xsl:attribute>
        <xsl:apply-templates select="./div[@type = &apos;protasis&apos;]"/>
        <xsl:apply-templates select="./div[@type = &apos;apodosis&apos;]"/>
</li>
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


  <xsl:template match="tei:body/tei:div/div[@n]/ab[@type = &apos;transcription&apos;]">
    <xsl:variable name="rdgid" select="../@n"/>
<li class="list-group-item border-0 p-1">
      <xsl:for-each select="../../div[@type = &apos;score&apos;]/ab/w">
        <xsl:sort select="./@xml:id"/>
        <!-- <xsl:for-each select="//tei:body/tei:div/div[@type = &apos;score&apos;]/ab/w"> -->
        <xsl:variable name="wordid" select="./@xml:id"/>
        <span>
          <xsl:value-of select="../../../div[@n=$rdgid]/ab[@type = &apos;transcription&apos;]/w[@corresp=$wordid]"/>
        </span>
        <xsl:text> </xsl:text>
      </xsl:for-each>
</li>
  </xsl:template>


</xsl:stylesheet>
