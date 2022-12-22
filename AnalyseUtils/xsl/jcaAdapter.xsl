<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0" xmlns:oracle-xsl-mapper="http://www.oracle.com/xsl/mapper/schemas"
                xmlns:oraxsl="http://www.oracle.com/XSL/Transform/java"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns="http://xmlns.darwin-it.nl/xsd/adapter/metadata" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:ns0="http://platform.integration.oracle/blocks/adapter/fw/metadata"
                exclude-result-prefixes="oracle-xsl-mapper xsi xsd xsl ns0 tns oraxsl"
                xmlns:tns="http://xmlns.darwin-it.nl/xsd/adapter/metadata">
  <oracle-xsl-mapper:schema>
    <!--SPECIFICATION OF MAP SOURCES AND TARGETS, DO NOT MODIFY.-->
    <oracle-xsl-mapper:mapSources>
      <oracle-xsl-mapper:source type="XSD">
        <oracle-xsl-mapper:schema location="../xsd/jcaAdapter.xsd"/>
        <oracle-xsl-mapper:rootElement name="adapter-config"
                                       namespace="http://platform.integration.oracle/blocks/adapter/fw/metadata"/>
      </oracle-xsl-mapper:source>
    </oracle-xsl-mapper:mapSources>
    <oracle-xsl-mapper:mapTargets>
      <oracle-xsl-mapper:target type="XSD">
        <oracle-xsl-mapper:schema location="../xsd/jcaAdapterProps.xsd"/>
        <oracle-xsl-mapper:rootElement name="adapter-config"
                                       namespace="http://xmlns.darwin-it.nl/xsd/adapter/metadata"/>
      </oracle-xsl-mapper:target>
    </oracle-xsl-mapper:mapTargets>
    <!--GENERATED BY ORACLE XSL MAPPER 12.2.1.3.0(XSLT Build 180705.1130.0048) AT [TUE NOV 27 14:03:09 CET 2018].-->
  </oracle-xsl-mapper:schema>
  <!--User Editing allowed BELOW this line - DO NOT DELETE THIS LINE-->
  <xsl:template match="/">
    <xsl:apply-templates select="/ns0:adapter-config"/>
  </xsl:template>
  <xsl:template match="ns0:adapter-config">
    <adapter-config name="{@name}" adapter="{@adapter}" wsdlLocation="{@wsdlLocation}">
      <connection-factory location="{ns0:connection-factory/@location}"
                          adapterRef="{ns0:connection-factory/@adapterRef}"/>
      <xsl:apply-templates select="ns0:endpoint-interaction[string-length(@operation)>0]"/>
      <xsl:apply-templates select="ns0:endpoint-activation[string-length(@operation)>0]"/>
    </adapter-config>
  </xsl:template>
  <!-- Endpoint Interaction Template -->
  <xsl:template match="ns0:endpoint-interaction">
    <endpoint portType="{@portType}" operation="{@operation}">
      <xsl:call-template name="addEndpointSpec">
        <xsl:with-param name="spec" select="ns0:interaction-spec"/>
        <xsl:with-param name="specType" select='"interaction"'/>
      </xsl:call-template>
    </endpoint>
  </xsl:template>
  <!-- Endpoint Activation Template -->
  <xsl:template match="ns0:endpoint-activation">
    <endpoint portType="{@portType}" operation="{@operation}">
      <xsl:call-template name="addEndpointSpec">
        <xsl:with-param name="spec" select="ns0:activation-spec"/>
        <xsl:with-param name="specType" select='"activation"'/>
      </xsl:call-template>
    </endpoint>
  </xsl:template>
  <!-- Endpoint Spec Properties -->
  <xsl:template name="addEndpointSpec">
    <xsl:param name="spec"/>
    <xsl:param name="specType"/>
    <spec className="{$spec/@className}" type="{$specType}">
      <!-- AQ/JMS -->
      <DestinationName>
        <xsl:value-of select="$spec/ns0:property[@name='DestinationName']/@value"/>
      </DestinationName>
      <DeliveryMode>
        <xsl:value-of select="ns0:property[@name='DeliveryMode']/@value"/>
      </DeliveryMode>
      <TimeToLive>
        <xsl:value-of select="ns0:property[@name='TimeToLive']/@value"/>
      </TimeToLive>
      <UseMessageListener>
        <xsl:value-of select="$spec/ns0:property[@name='UseMessageListener']/@value"/>
      </UseMessageListener>
      <MessageSelector>
        <xsl:value-of select="$spec/ns0:property[@name='MessageSelector']/@value"/>
      </MessageSelector>
      <PayloadType>
        <xsl:value-of select="$spec/ns0:property[@name='PayloadType']/@value"/>
      </PayloadType>
      <QueueName>
        <xsl:value-of select="$spec/ns0:property[@name='QueueName']/@value"/>
      </QueueName>
      <ObjectFieldName>
        <xsl:value-of select="$spec/ns0:property[@name='ObjectFieldName']/@value"/>
      </ObjectFieldName>
      <PayloadHeaderRequired>
        <xsl:value-of select="$spec/ns0:property[@name='PayloadHeaderRequired']/@value"/>
      </PayloadHeaderRequired>
      <RecipientList>
        <xsl:value-of select="ns0:property[@name='RecipientList']/@value"/>
      </RecipientList>
      <Consumer>
        <xsl:value-of select="$spec/ns0:property[@name='Consumer']/@value"/>
      </Consumer>
      <!-- File/FTP -->
      <ChunkSize>
        <xsl:value-of select="$spec/ns0:property[@name='ChunkSize']/@value"/>
      </ChunkSize>
      <NumberMessages>
        <xsl:value-of select="$spec/ns0:property[@name='NumberMessages']/@value"/>
      </NumberMessages>
      <Append>
        <xsl:value-of select="$spec/ns0:property[@name='Append']/@value"/>
      </Append>
      <FileName>
        <xsl:value-of select="$spec/ns0:property[@name='FileName']/@value"/>
      </FileName>
      <FileType>
        <xsl:value-of select="$spec/ns0:property[@name='FileType']/@value"/>
      </FileType>
      <FileNamingConvention>
        <xsl:value-of select="$spec/ns0:property[@name='FileNamingConvention']/@value"/>
      </FileNamingConvention>
      <LogicalDirectory>
        <xsl:value-of select="$spec/ns0:property[@name='LogicalDirectory']/@value"/>
      </LogicalDirectory>
      <LogicalArchiveDirectory>
        <xsl:value-of select="$spec/ns0:property[@name='LogicalArchiveDirectory']/@value"/>
      </LogicalArchiveDirectory>
      <UseRemoteErrorArchive>
        <xsl:value-of select="$spec/ns0:property[@name='UseRemoteErrorArchive']/@value"/>
      </UseRemoteErrorArchive>
      <UseRemoteArchive>
        <xsl:value-of select="$spec/ns0:property[@name='UseRemoteArchive']/@value"/>
      </UseRemoteArchive>
      <UseHeaders>
        <xsl:value-of select="$spec/ns0:property[@name='UseHeaders']/@value"/>
      </UseHeaders>
      <PhysicalErrorArchiveDirectory>
        <xsl:value-of select="$spec/ns0:property[@name='PhysicalErrorArchiveDirectory']/@value"/>
      </PhysicalErrorArchiveDirectory>
      <MinimumAge>
        <xsl:value-of select="$spec/ns0:property[@name='MinimumAge']/@value"/>
      </MinimumAge>
      <Recursive>
        <xsl:value-of select="$spec/ns0:property[@name='Recursive']/@value"/>
      </Recursive>
      <PollingFrequency>
        <xsl:value-of select="$spec/ns0:property[@name='PollingFrequency']/@value"/>
      </PollingFrequency>
      <DeleteFile>
        <xsl:value-of select="$spec/ns0:property[@name='DeleteFile']/@value"/>
      </DeleteFile>
      <IncludeFiles>
        <xsl:value-of select="$spec/ns0:property[@name='IncludeFiles']/@value"/>
      </IncludeFiles>
      <!-- File/FTP Move -->
      <SourcePhysicalDirectory>
        <xsl:value-of select="$spec/ns0:property[@name='SourcePhysicalDirectory']/@value"/>
      </SourcePhysicalDirectory>
      <SourceFileName>
        <xsl:value-of select="$spec/ns0:property[@name='SourceFileName']/@value"/>
      </SourceFileName>
      <SourceIsRemote>
        <xsl:value-of select="$spec/ns0:property[@name='SourceIsRemote']/@value"/>
      </SourceIsRemote>
      <TargetPhysicalDirectory>
        <xsl:value-of select="$spec/ns0:property[@name='TargetPhysicalDirectory']/@value"/>
      </TargetPhysicalDirectory>
      <TargetFileName>
        <xsl:value-of select="$spec/ns0:property[@name='TargetFileName']/@value"/>
      </TargetFileName>
      <Type>
        <xsl:value-of select="$spec/ns0:property[@name='Type']/@value"/>
      </Type>
      <!-- Database -->
      <SchemaName>
        <xsl:value-of select="$spec/ns0:property[@name='SchemaName']/@value"/>
      </SchemaName>
      <PackageName>
        <xsl:value-of select="$spec/ns0:property[@name='PackageName']/@value"/>
      </PackageName>
      <ProcedureName>
        <xsl:value-of select="$spec/ns0:property[@name='ProcedureName']/@value"/>
      </ProcedureName>
      <GetActiveUnitOfWork>
        <xsl:value-of select="$spec/ns0:property[@name='GetActiveUnitOfWork']/@value"/>
      </GetActiveUnitOfWork>
      <DescriptorName>
        <xsl:value-of select="$spec/ns0:property[@name='DescriptorName']/@value"/>
      </DescriptorName>
      <DmlType>
        <xsl:value-of select="$spec/ns0:property[@name='DmlType']/@value"/>
      </DmlType>
      <MappingsMetaDataURL>
        <xsl:value-of select="$spec/ns0:property[@name='MappingsMetaDataURL']/@value"/>
      </MappingsMetaDataURL>
      <DetectOmissions>
        <xsl:value-of select="$spec/ns0:property[@name='DetectOmissions']/@value"/>
      </DetectOmissions>
      <SqlString>
        <xsl:value-of select="$spec/ns0:property[@name='SqlString']/@value"/>
      </SqlString>
      <QueryName>
        <xsl:value-of select="$spec/ns0:property[@name='QueryName']/@value"/>
      </QueryName>
      <PollingStrategy>
        <xsl:value-of select="$spec/ns0:property[@name='PollingStrategy']/@value"/>
      </PollingStrategy>
      <PollingInterval>
        <xsl:value-of select="$spec/ns0:property[@name='PollingInterval']/@value"/>
      </PollingInterval>
      <MaxRaiseSize>
        <xsl:value-of select="$spec/ns0:property[@name='MaxRaiseSize']/@value"/>
      </MaxRaiseSize>
      <MaxTransactionSize>
        <xsl:value-of select="$spec/ns0:property[@name='MaxTransactionSize']/@value"/>
      </MaxTransactionSize>
      <NumberOfThreads>
        <xsl:value-of select="$spec/ns0:property[@name='NumberOfThreads']/@value"/>
      </NumberOfThreads>
      <ReturnSingleResultSet>
        <xsl:value-of select="$spec/ns0:property[@name='ReturnSingleResultSet']/@value"/>
      </ReturnSingleResultSet>
    </spec>
  </xsl:template>
</xsl:stylesheet>