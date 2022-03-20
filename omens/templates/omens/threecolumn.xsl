<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0">
    <xsl:param name="omen"/>


    <xsl:key name="witness"
        match="tei:body/tei:div/tei:div[@type = &apos;score&apos;]/tei:ab/tei:w/tei:app/tei:rdg"
        use="./@wit"/>
    <xsl:key name="source"
        match="tei:body/tei:div/tei:div[@type = &apos;score&apos;]/tei:ab/tei:w/tei:app/tei:rdg"
        use="./@source"/>
    <xsl:template match="/">
        <div id="omens">
            <div class="table-responsive">
                <table class="table-striped table-condensed">
                    <tbody> 
                            <xsl:variable name="final">'</xsl:variable>
                            <xsl:variable name="i"> i </xsl:variable> <xsl:variable name="ii"> ii </xsl:variable> <xsl:variable name="iii"> iii </xsl:variable>
                            <xsl:variable name="iv"> iv </xsl:variable> <xsl:variable name="v"> v </xsl:variable><xsl:variable name="vi"> vi </xsl:variable>
                        <xsl:choose>
                            <xsl:when test="not($omen)">
                             <!-- parameter has not been supplied -->
                                <!-- All Omens -->
                               <xsl:apply-templates select=".//tei:body/tei:div[not(contains(./@n, 'N') or contains(./@n, 'A') or contains(./@n, 'S'))]">
                                    <!-- A) plain omen series -->
                                    <xsl:sort select="substring-after(translate(translate(./@n, 'ab', ''), $final, ''), '.')" data-type="number"/> 
                                </xsl:apply-templates> 
                                <xsl:apply-templates select=".//tei:body/tei:div[string-length (./@n) &lt; 15 and (contains(./@n, 'N') or contains(./@n, 'A') or contains(./@n, 'S'))]">
                                    <!-- B) omen series, only place siglum -->
                                    <xsl:sort select="substring(./@n, 9, 1)" data-type="text" /> <!-- by letter-ID after chapter no. -->
                                    <xsl:sort select="substring(translate(./@n, $final, ''), 11, 3)" data-type="number" />
                                    </xsl:apply-templates> 
                                <xsl:apply-templates select=".//tei:body/tei:div[string-length (./@n) &gt; 15 and (contains(./@n, 'N') or contains(./@n, 'A') or contains(./@n, 'S'))]">
                                    <!-- B) very tricky omen series: place siglum and museum no. -->
                                    <xsl:sort select="substring(./@n, 9, 1)" data-type="text" /> <!-- by letter-ID after chapter no. -->
                                    <xsl:sort select="substring(./@n, 11, 1)" data-type="text" /> <!-- by letter of museum siglum -->
                                    <xsl:sort select="substring(./@n, 13, 6)"  /> <!-- by museum no. as string (because of .1 var.s) -->
                                    <xsl:sort select="contains(./@n, $vi) "/> <xsl:sort select="contains(./@n, $v) "/><xsl:sort select="contains(./@n, $iv) "/>
                                    <xsl:sort select="contains(./@n, $iii) "/><xsl:sort select="contains(./@n, $ii) "/> <xsl:sort select="contains(./@n, $i)"/>
                                    <xsl:sort select="substring(translate(translate(translate(./@n, '+', ' '), 'abi', ''), $final, ''), string-length(./@n)-3)" data-type="number" />
                                </xsl:apply-templates>
                            </xsl:when>
                            <xsl:otherwise>
                                <!--parameter has been supplied -->
                                <xsl:apply-templates select=".//tei:body/tei:div[@xml:id = $omen]"/>
                                <!-- Omen -->
                            </xsl:otherwise>
                        </xsl:choose>
                    </tbody>
                </table>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="tei:body/tei:div">

        <!-- </xsl:choose> -->

        <xsl:apply-templates select="./tei:div[@type = &apos;score&apos;]"/>
        <!-- Score -->
        <xsl:apply-templates select="./tei:div[@n]"/>
        <!-- Reconstruction -->
    </xsl:template>

    <xsl:template match="tei:body/tei:div/tei:div[@type = &apos;score&apos;]">
        <!-- Score -->
        <xsl:variable name="omenid" select="../@xml:id"/>
        <xsl:variable name="headerid" select="../@n"/>
        <tr>
            <th colspan="100%">
                <xsl:choose>
                    <xsl:when test="not($omen)">
                        <!-- parameter has not been supplied -->
                        <a target="_blank" class="btn-sm btn-link text-decoration-none">
                            <xsl:attribute name="href">/omens/<xsl:value-of select="$omenid"
                                />/tei</xsl:attribute> &#8599; </a>
                                <xsl:value-of select="substring-after($headerid, 'Omen ')"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <a target="_blank" class="btn-sm btn-link text-decoration-none">
                            <xsl:attribute name="href">/omens/<xsl:value-of select="$omenid"
                                />/tei.xml</xsl:attribute> &#8595; </a>
                    <xsl:value-of select="substring-after($headerid, 'Omen ')"/>&#160; <a
                    data-toggle="collapse" role="button" aria-expanded="false">
                    <xsl:attribute name="data-target">.<xsl:value-of select="$omenid"
                        />-score-row</xsl:attribute>
                    <xsl:attribute name="href">#<xsl:value-of select="$omenid"
                        />-score</xsl:attribute>
                    <small>Score</small>
                    </a>
                    </xsl:otherwise>
                </xsl:choose>
            </th>
        </tr>
        <xsl:if test="$omen">
        <tr>
            <xsl:attribute name="class">small <xsl:value-of select="$omenid"/>-score-row
                collapse</xsl:attribute>
            <td colspan="100%">
                <table class="table-condensed score-table">   
                    <xsl:for-each select="//tei:witness">
                        <xsl:variable name="witid" select="./tei:idno"/>
                        <xsl:if test="//*[@xml:id = $omenid]//tei:rdg[@wit = $witid]">
                            <!-- if witness is used in the score -->
                            <tr>
                                <td>
                                    <b><xsl:value-of select="./tei:idno"/></b>
                                </td>
                                <td>
                                </td>
                                <td>
                                    <em>
                                        <xsl:value-of
                                            select="//*[@xml:id = $omenid]/tei:div[@type = &apos;score&apos;]/tei:ab/tei:cb[@ed = $witid]/@n"
                                        /> &#160;
                                    </em>
                                    <em>
                                        <xsl:value-of
                                            select="//*[@xml:id = $omenid]/tei:div[@type = &apos;score&apos;]/tei:ab/tei:lb[@ed = $witid]/@n"
                                        />
                                    </em>
                                </td>  
                                <xsl:for-each
                                    select="//*[@xml:id = $omenid]/tei:div[@type = &apos;score&apos;]/tei:ab/tei:w">
                                    <xsl:sort select="./@xml:id"/>
                                    <td>
                                        <xsl:apply-templates
                                            select="tei:app/tei:rdg[(@wit = $witid) and not(@source)]"
                                        />
                                    </td>
                                </xsl:for-each>
                            </tr>

                            <xsl:for-each
                                select="//*[generate-id() = generate-id(key('source', @source)[1])]">
                                <tr>
                                    <xsl:if
                                        test="@source = //*[@xml:id = $omenid]/tei:div[@type = &apos;score&apos;]/tei:ab/tei:w/tei:app/tei:rdg[(@wit = $witid)]/@source">
                                        <td>
                                            <xsl:value-of select="$witid"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="@source"/>
                                        </td>
                                        <td>
                                    <em>
                                        <xsl:value-of
                                            select="//*[@xml:id = $omenid]/tei:div[@type = &apos;score&apos;]/tei:ab/tei:cb[@ed = $witid]/@n"
                                        />&#160;
                                    </em>
                                    <em>
                                        <xsl:value-of
                                            select="//*[@xml:id = $omenid]/tei:div[@type = &apos;score&apos;]/tei:ab/tei:lb[@ed = $witid]/@n"
                                        />
                                    </em>
                                </td>
                                        <xsl:variable name="src" select="@source"/>
                                        <xsl:for-each
                                            select="//*[@xml:id = $omenid]/tei:div[@type = &apos;score&apos;]/tei:ab/tei:w">
                                            <xsl:sort select="./@xml:id"/>
                                            <td>
                                                <xsl:apply-templates
                                                  select="tei:app/tei:rdg[(@wit = $witid) and (@source = $src)]"
                                                />
                                            </td>
                                        </xsl:for-each>
                                    </xsl:if>
                                </tr>
                            </xsl:for-each>

                        </xsl:if>
                    </xsl:for-each>
                </table>
            </td>
        </tr>
        </xsl:if>
    </xsl:template>

    <xsl:template match="tei:anchor">
        <xsl:choose>
            <xsl:when test="@type = 'breakStart'">
                <xsl:text>[</xsl:text>
            </xsl:when>
            <xsl:when test="@type = 'breakEnd'">
                <xsl:if test="../tei:damageSpan">
                    <xsl:text>&#11811;</xsl:text>
                </xsl:if>
                <xsl:if test="not(../tei:damageSpan)">
                    <xsl:text>]</xsl:text>
                </xsl:if>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:damageSpan">
        <xsl:text>&#11810;</xsl:text>
    </xsl:template>

    <xsl:template match="tei:rdg/text()">
        <xsl:choose>
            <xsl:when test="contains(., '#')">
                <em><xsl:value-of
                    select="translate(., '#', ' ')"
                /></em>
            </xsl:when>
            <xsl:when test="contains(., '}')">
                <xsl:variable name="before" select="substring-before(., '{')"/>
                <xsl:variable name="after" select="substring-after(., '}')"/>
                <xsl:variable name="until" select="substring-before(., '}')"/>
                <xsl:variable name="super" select="substring-after($until, '{')"/>
                <xsl:value-of select="$before"/>
                <xsl:element name="sup">
                    <xsl:value-of select="$super"/>
                </xsl:element>
                <xsl:value-of select="$after"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of
                    select="translate(., '012345678911', '&#8320;&#8321;&#8322;&#8323;&#8324;&#8325;&#8326;&#8327;&#8328;&#8329;&#83211;')"
                />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="tei:body/tei:div/tei:div[@type = &apos;score&apos;]/tei:ab/tei:w">
        <!-- Words in the score -->
        <th scope="col">
            <small>
                <xsl:value-of select="@xml:id"/>
            </small>
        </th>
    </xsl:template>

    <xsl:template match="tei:body/tei:div/tei:div[@n]">
        <!-- Reconstruction -->
        <tr>
            <td class="reconstruction-label">
                <xsl:value-of select="@n"/>
                <xsl:if test="*[@source]">
                    <div class="form-check form-check-inline">
                        <input class="form-check-input" type="checkbox" value="others">
                            <xsl:attribute name="id">
                                <xsl:value-of select="./@xml:id"/>-others </xsl:attribute>
                            <xsl:attribute name="onclick"> toggleClass&#x28;this,&apos;<xsl:value-of
                                    select="./@xml:id"/>-others&apos;&#x29; </xsl:attribute>
                        </input>
                        <label class="form-check-label">
                            <xsl:attribute name="for">
                                <xsl:value-of select="./@xml:id"/>-others </xsl:attribute>
                            <small class="text-muted">Previous readings and translations</small>
                        </label>
                    </div>
                </xsl:if>
            </td>
            <td class="transliteration">
                <ul class="list-group">
                    <xsl:apply-templates select="./tei:ab[@type = &apos;transliteration&apos;]"/>
                </ul>
            </td>
            <td class="transcription">
                <ul class="list-group">
                    <xsl:apply-templates select="./tei:ab[@type = &apos;transcription&apos;]"/>
                </ul>
            </td>
            <td class="translation">
                <ul class="list-group">
                    <xsl:apply-templates select="./tei:ab[@type = &apos;translation&apos;]"/>
                </ul>
            </td>
        </tr>
    </xsl:template>

    <xsl:template match="tei:body/tei:div/tei:div[@n]/tei:ab[@type = &apos;translation&apos;]">
        <!-- <th scope="row">Translation (<xsl:value-of select="@lang"/>)</th> -->
        <li class="list-group-item">
            <xsl:attribute name="xml:lang">
                <xsl:value-of select="@xml:lang"/>
            </xsl:attribute>
            <xsl:choose>
                <xsl:when test="@source">
                    <xsl:attribute name="class">list-group-item <xsl:value-of select="../@xml:id"
                        />-others others d-none </xsl:attribute>
                    <xsl:value-of select="@source"/>
                </xsl:when>
            </xsl:choose>
            <div>
                <xsl:attribute name="id">
                    <xsl:value-of select="./@xml:id"/>
                </xsl:attribute>
                <xsl:apply-templates select="./tei:seg[@type = &apos;protasis&apos; and not(@n)]"/>
                <xsl:apply-templates select="./tei:seg[@type = &apos;apodosis&apos; and not(@n)]"/>
                <xsl:apply-templates select="./tei:seg[(@type = &apos;protasis&apos; or @type = &apos;apodosis&apos;) and @n]">
                    <xsl:sort select="./@n" order="ascending" data-type="number"/>
                </xsl:apply-templates>
            </div>
        </li>
    </xsl:template>

    <xsl:template match="tei:body/tei:div/tei:div[@n]/tei:ab[@type = &apos;transliteration&apos;]">
        <xsl:variable name="rdgid" select="../@n"/>
        <xsl:variable name="rdgxmlid" select="@xml:id"/>
        <!-- <xsl:value-of select="@xml:id"/> -->
        <!-- <th scope="row">Transliteration</th> -->
        <li class="list-group-item">
            <xsl:choose>
                <xsl:when test="@source">
                    <xsl:attribute name="class">list-group-item <xsl:value-of select="../@xml:id"
                        />-others others d-none</xsl:attribute>
                    <xsl:value-of select="@source"/>
                </xsl:when>
            </xsl:choose>
            <div>
                <xsl:attribute name="id">
                    <xsl:value-of select="./@xml:id"/>
                </xsl:attribute>
                <xsl:for-each select="../../tei:div[@type = &apos;score&apos;]/tei:ab/tei:w">
                    <xsl:sort select="./@xml:id"/>
                    <!-- <xsl:for-each select="//tei:body/tei:div/tei:div[@type = &apos;score&apos;]/tei:ab/tei:w"> -->
                    <xsl:variable name="wordid" select="./@xml:id"/>
                    <span class="lemma">
                        <xsl:apply-templates
                            select="../../../tei:div[@n = $rdgid]/tei:ab[@xml:id = $rdgxmlid]/tei:w[@corresp = $wordid]"
                        />
                    </span>
                </xsl:for-each>
            </div>
        </li>
    </xsl:template>

    <xsl:template match="tei:div/tei:ab[@type = 'transliteration' or @type = 'transcription']/tei:w/text()">
        <xsl:choose>
            <xsl:when test="contains(., '#')">
                <em><xsl:value-of
                    select="translate(., '#', ' ')"
                /></em>
            </xsl:when>
            <xsl:when test="contains(., '}')">
                <xsl:variable name="before" select="substring-before(., '{')"/>
                <xsl:variable name="after" select="substring-after(., '}')"/>
                <xsl:variable name="until" select="substring-before(., '}')"/>
                <xsl:variable name="super" select="substring-after($until, '{')"/>
                <xsl:value-of select="$before"/>
                <xsl:element name="sup">
                    <xsl:value-of select="$super"/>
                </xsl:element>
                <xsl:value-of select="$after"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of
                    select="translate(., '012345678911', '&#8320;&#8321;&#8322;&#8323;&#8324;&#8325;&#8326;&#8327;&#8328;&#8329;&#83211;')"
                />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:div/tei:ab[@type = 'translation']/tei:seg[@type = &apos;protasis&apos; or @type = &apos;apodosis&apos;]">
        <xsl:variable name="tran" select="."/>
        <xsl:variable name="question">?</xsl:variable>
 
        <xsl:choose>
            <xsl:when test="contains(., '$')">
                <xsl:call-template name="recursionItalics">
                    <xsl:with-param name="translation" select="$tran"/>
                </xsl:call-template>
            </xsl:when>
           <xsl:when test="contains(., $question)">
                <xsl:call-template name="recursionSuper">
                    <xsl:with-param name="translation" select="$tran"/>
                </xsl:call-template>
            </xsl:when> 
            <xsl:otherwise>
                <xsl:value-of select="$tran"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="recursionSuper" match="tei:div/tei:ab[@type = 'translation']/tei:seg[@type = &apos;protasis&apos; or @type = &apos;apodosis&apos;]/text()">
        <xsl:param name="translation"/>
        
        <xsl:variable name="question">?</xsl:variable>
        <xsl:variable name="before" select="substring-before($translation, '{')"/>
        <xsl:variable name="after" select="substring-after($translation, '}')"/>
        
        <xsl:value-of select="$before"/>
        <xsl:element name="sup">
            <xsl:value-of select="$question"/>
        </xsl:element>
        <xsl:choose>
            <xsl:when test="contains($after, $question)">
                <xsl:call-template name="recursionSuper">
                    <xsl:with-param name="translation" select="$after"/>
                </xsl:call-template> 
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$after"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="recursionItalics" match="tei:div/tei:ab[@type = 'translation']/tei:seg[@type = &apos;protasis&apos; or @type = &apos;apodosis&apos;]/text()">
        <xsl:param name="translation"/>
        <xsl:variable name="italics">$</xsl:variable>
        <xsl:variable name="question">{?}</xsl:variable>
        
        <xsl:variable name="before" select="substring-before($translation, '$')"/>
        <xsl:variable name="after" select="substring-after($translation, '/$')"/>
        <xsl:variable name="replace" select="substring-before(substring-after($translation, '$'), '/$')"/>
        
        <xsl:value-of select="$before"/>
        <xsl:element name="em">
            <xsl:value-of select="$replace"/>
        </xsl:element>
       <xsl:choose>
            <xsl:when test="contains($after, $italics)">
                <xsl:call-template name="recursionItalics">
                    <xsl:with-param name="translation" select="translate($after, $question, '?')"/>
                </xsl:call-template> 
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$after"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:body/tei:div/tei:div[@n]/tei:ab[@type = &apos;transcription&apos;]">
        <xsl:variable name="rdgid" select="../@n"/>
        <xsl:variable name="rdgxmlid" select="@xml:id"/>
        <!-- <th scope="row">Transcription</th> -->
        <li class="list-group-item">
            <xsl:choose>
                <xsl:when test="@source">
                    <xsl:attribute name="class">list-group-item <xsl:value-of select="../@xml:id"
                        />-others others d-none</xsl:attribute>
                    <xsl:value-of select="@source"/>
                </xsl:when>
            </xsl:choose>
            <div>
                <xsl:attribute name="id">
                    <xsl:value-of select="./@xml:id"/>
                </xsl:attribute>
                <xsl:for-each select="../../tei:div[@type = &apos;score&apos;]/tei:ab/tei:w">
                    <xsl:sort select="./@xml:id"/>
                    <xsl:variable name="wordid" select="./@xml:id"/>
                    <span class="lemma">
                        <xsl:apply-templates
                            select="../../../tei:div[@n = $rdgid]/tei:ab[@xml:id = $rdgxmlid]/tei:w[@corresp = $wordid]"
                        />
                    </span>
                </xsl:for-each>
            </div>
        </li>
    </xsl:template>

</xsl:stylesheet>