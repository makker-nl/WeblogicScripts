<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:src="http://xmlns.oracle.com/bpel/sensor"
                xmlns:oracle-xsl-mapper="http://www.oracle.com/xsl/mapper/schemas"
                xmlns:tns="http://xmlns.darwin-it.nl/bpel/sensor"
                xmlns:oraxsl="http://www.oracle.com/XSL/Transform/java"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                exclude-result-prefixes="oracle-xsl-mapper xsi xsd xsl src tns oraxsl">
  <oracle-xsl-mapper:schema>
    <!--SPECIFICATION OF MAP SOURCES AND TARGETS, DO NOT MODIFY.-->
    <oracle-xsl-mapper:mapSources>
      <oracle-xsl-mapper:source type="XSD">
        <oracle-xsl-mapper:schema location="../xsd/sensors.xsd"/>
        <oracle-xsl-mapper:rootElement name="sensors" namespace="http://xmlns.oracle.com/bpel/sensor"/>
      </oracle-xsl-mapper:source>
    </oracle-xsl-mapper:mapSources>
    <oracle-xsl-mapper:mapTargets>
      <oracle-xsl-mapper:target type="XSD">
        <oracle-xsl-mapper:schema location="../xsd/sensorsProps.xsd"/>
        <oracle-xsl-mapper:rootElement name="sensors" namespace="http://xmlns.darwin-it.nl/bpel/sensor"/>
      </oracle-xsl-mapper:target>
    </oracle-xsl-mapper:mapTargets>
    <!--GENERATED BY ORACLE XSL MAPPER 12.2.1.3.0(XSLT Build 180705.1130.0048) AT [TUE JAN 14 14:44:24 CET 2020].-->
  </oracle-xsl-mapper:schema>
  <!--User Editing allowed BELOW this line - DO NOT DELETE THIS LINE-->
  <xsl:template match="/">
    <!-- Important: for the ANT task xmlproperty the elements cannot be prefixed with a namespace shortage! -->
    <sensors>
      <xsl:for-each select="/src:sensors/src:sensor">
        <xsl:element name="{@sensorName}">
          <xsl:if test="@kind">
            <xsl:attribute name="kind">
              <xsl:value-of select="@kind"/>
            </xsl:attribute>
          </xsl:if>
          <xsl:if test="@target">
            <xsl:attribute name="target">
              <xsl:value-of select="@target"/>
            </xsl:attribute>
          </xsl:if>
          <variableList>
            <xsl:call-template name="listVariables">
              <xsl:with-param name="activityConfig" select="src:activityConfig"/>
              <xsl:with-param name="index" select='1'/>
            </xsl:call-template>
          </variableList>
          <activityConfig>
            <xsl:if test="src:activityConfig/@evalTime">
              <xsl:attribute name="evalTime">
                <xsl:value-of select="src:activityConfig/@evalTime"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:for-each select="src:activityConfig/src:variable">
              <variable>
                <xsl:if test="@outputDataType">
                  <xsl:attribute name="outputDataType">
                    <xsl:value-of select="@outputDataType"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="@outputNamespace">
                  <xsl:attribute name="outputNamespace">
                    <xsl:value-of select="@outputNamespace"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="@target">
                  <xsl:attribute name="target">
                    <xsl:value-of select="@target"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:value-of select="."/>
              </variable>
            </xsl:for-each>
          </activityConfig>
        </xsl:element>
      </xsl:for-each>
      <sensorList>
        <xsl:call-template name="listSensors">
          <xsl:with-param name="sensors" select="/src:sensors"/>
          <xsl:with-param name="index" select='1'/>
        </xsl:call-template>
      </sensorList>
    </sensors>
  </xsl:template>
  <!-- Create a ;-delimited list of sensor names to loop over -->
  <xsl:template name="listSensors">
    <xsl:param name="sensors"/>
    <xsl:param name="index"/>
    <xsl:variable name="countSensors" select="count($sensors/src:sensor)"/>
    <xsl:choose>
      <xsl:when test="$index=1">
        <xsl:value-of select="$sensors/src:sensor[$index]/@sensorName"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="concat(';',$sensors/src:sensor[$index]/@sensorName)"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="$index &lt; $countSensors">
      <xsl:call-template name="listSensors">
        <xsl:with-param name="sensors" select="$sensors"/>
        <xsl:with-param name="index" select='$index+1'/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
  <!-- Create a |-delimited list of sensor names to put in the CSV file.
  !!! Important: this is | delimited, because Excel interprets ; as a delimiter, even when not selected as an option !!!
  -->
  <xsl:template name="listVariables">
    <xsl:param name="activityConfig"/>
    <xsl:param name="index"/>
    <xsl:variable name="countVariables" select="count($activityConfig/src:variable)"/>
    <xsl:choose>
      <xsl:when test="$index=1">
        <xsl:value-of select="$activityConfig/src:variable[$index]/@target"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="concat('|',$activityConfig/src:variable[$index]/@target)"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="$index &lt; $countVariables">
      <xsl:call-template name="listVariables">
        <xsl:with-param name="activityConfig" select="$activityConfig"/>
        <xsl:with-param name="index" select='$index+1'/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
