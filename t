('{"type":"record","name":"EmptyData","namespace":"org.kaaproject.kaa.schema.system","fields":[{"name":"__uuid","type":[{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"null"],"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Empty Data","description":"Auto generated"}',
                                           '
'{"type":"record","name":"EmptyData","namespace":"org.kaaproject.kaa.schema.system","fields":[{"name":"__uuid","type":[{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"null"],"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Empty Data","description":"Auto generated"}',

'{"type":"array","items":{"type":"record","name":"deltaT","namespace":"org.kaaproject.configuration","fields":[{"name":"delta","type":[{"type":"record","name":"EmptyData","namespace":"org.kaaproject.kaa.schema.system","fields":[{"name":"__uuid","type":{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Empty Data","description":"Auto generated"}]}]}}',

2),


('{"type":"record","name":"Configuration","namespace":"org.kaaproject.kaa.schema.sample","fields":[{"name":"samplePeriod","type":"int","by_default":1},{"name":"__uuid","type":[{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"null"],"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Configuration Schemas"}',

'{"type":"record","name":"Configuration","namespace":"org.kaaproject.kaa.schema.sample","fields":[{"name":"samplePeriod","type":["int",{"type":"enum","name":"unchangedT","namespace":"org.kaaproject.configuration","symbols":["unchanged"]}],"by_default":1},{"name":"__uuid","type":[{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},"null"],"displayName":"Record Id","fieldAccess":"read_only"}],"version":1,"displayName":"Configuration Schemas"}',


,7);

{
	"type":"array",
	"items":{	
		"type":"record",
		"name":"deltaT",
		"namespace":"org.kaaproject.configuration",
		"fields":[
			{
				"name":"delta",
            	"type":[
					{
						"type":"record",
						"name":"Configuration",
						"namespace":"org.kaaproject.kaa.schema.sample",
						"fields":[
							{
								"name":"samplePeriod",
								"type":["int",{"type":"enum","name":"unchangedT","namespace":"org.kaaproject.configuration","symbols":["unchanged"]}],
								"by_default":1
 							},
							{
								"name":"__uuid",
								"type":{"type":"fixed","name":"uuidT","namespace":"org.kaaproject.configuration","size":16},
								"displayName":"Record Id",
								"fieldAccess":"read_only"
							}
						],
						"version":1,
						"displayName":"Configuration Schemas"
					}
				]
			}
		]
	}
}
