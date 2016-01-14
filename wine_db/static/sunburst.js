// Set width and height breakpoints.
var maxWidth = 700;
if (window.innerWidth < maxWidth) {
    maxWidth = window.innerWidth;
}

var maxHeight = 550;
if (window.innerHeight < maxHeight) {
    maxHeight = window.innerHeight - (window.innerHeight / 8);
}

var width = maxWidth,
    height = maxHeight + (maxHeight / 11 + 20),
    radius = Math.min(width, height - 20) / 2;

var x = d3.scale.linear()
    .range([0, 2 * Math.PI]);

var y = d3.scale.sqrt()
    .range([0, radius]);

var color = d3.scale.category20c('#F64740', '#2274A5', '#E83F6F');

// Mapping of step names to colors.
var colors = {
    "Red": "#DD1C1A",
    "White": "#00A6ED",
    "Rose": "#D90368",
    "Unknown": "#291720",
    "N\\A": "#000000"
};

var svg = d3.select("#sunburst").append("svg")
    .attr("width", width)
    .attr("height", height + 20)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2 ) + ")");

var partition = d3.layout.partition()
    .sort(null)
    .value(function (d) {
        return 1;
    });

var arc = d3.svg.arc()
    .startAngle(function (d) {
        return Math.max(0, Math.min(2 * Math.PI, x(d.x)));
    })
    .endAngle(function (d) {
        return Math.max(0, Math.min(2 * Math.PI, x(d.x + d.dx)));
    })
    .innerRadius(function (d) {
        return Math.max(0, y(d.y));
    })
    .outerRadius(function (d) {
        return Math.max(0, y(d.y + d.dy));
    });

// Keep track of the node that is currently being displayed as the root.
var node;

d3.json("data.json", function (error, root) {
    node = root;

    var data = svg.datum(root).selectAll("g")
        .data(partition.nodes(root));

    var group1 = data.enter().append("g").attr("class", "g-inner").filter(function (d) {
        return d.depth < 2;
    });


    var path = group1.append("path")
        .attr("d", arc)
        .attr('id', function (d) {
            return "sunburst_" + d.name;
        })
        .style("fill", function (d) {
            if (colors[d.name]) {
                return colors[d.name]
            } else {
                return color((d.children ? d : d.parent).name)
            }
        })
        .on("click", click)
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave)
        .each(stash);

    //Create an SVG text element and append a textPath element
/*    var text = group1.append("text")
        //.attr("x", function (d) {
        //    return d.x;
        //})   //Move the text from the start angle of the
     //    .attr("transform", function (d) {
     //return "rotate(" + computeTextRotation(d) + ")";
     //})
        .attr("dy", function (d) {
            return (d.dy*120);
        }) //Move the text down
        .append("textPath") //append a textPath to the text element
        .attr("xlink:href", function (d) {
            return "#sunburst_" + d.name;
        }) //place the ID of the path here
        .style("text-anchor", "middle") //place the text halfway on the arc
        .attr("fill", "white") //place the text halfway on the arc
        .attr("startOffset", "20%")
        //.attr('y', -20)

        .text(function (d) {
            return d.name;
        });*/
     var text = group1.append("text")
     .attr("transform", function (d) {
     return "rotate(" + computeTextRotation(d) + ")";
     })
     .attr("x", function (d) {
     return y(d.y);
     })
     //.attr("y", function (d) {
     //    return x(d.x);
     //})
     .attr("dx", "6") // margin
     .attr("dy", ".35em") // vertical-align
     .attr("fill", "white")
     .text(function (d) {
     return d.name;
     });

    var group2 = data.enter().append("g").filter(function (d) {
        return d.depth >= 2;
    }).attr("class", "g-outer");

    var path2 = group2.append("path")
        .attr("d", arc)
        .attr('id', function (d) {
            return "sunburst_" + d.name;
        })
        .style("fill", function (d) {
            if (colors[d.name]) {
                return colors[d.name]
            } else {
                return color((d.children ? d : d.parent).name)
            }
        })
        .on("click", click)
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave)
        .each(stash);

    svg.append("svg:text")
        .attr("x", "0")
        .attr("y", (maxHeight / 2) + (maxHeight / 12))
        .attr("fill", "black")
        .attr("stroke", "white")
        .attr("stroke-width", "0.5")
        .attr("font-size", "18")
        .attr("font-weight", "bold")
        .attr("font-family", "sans-serif")
        .attr("text-anchor", "middle")
        .attr("id", "sunburst_info");

    //d3.selectAll("input").on("change", function change() {
    //    var value = this.value === "count"
    //        ? function () {
    //        return 1;
    //    }
    //        : function (d) {
    //        return d.size;
    //    };
    //
    //    path
    //        .data(partition.value(value).nodes)
    //        .transition()
    //        .duration(1000)
    //        .attrTween("d", arcTweenData);
    //});

    function click(d) {
        node = d;

        console.group("Item");
        console.log(d);
        console.groupEnd();

        if (d.depth === 3) {
            path.transition()
                .duration(1000)
                .attrTween("d", arcTweenZoom(d.parent));

            path2.transition()
                .duration(1000)
                .attrTween("d", arcTweenZoom(d.parent));
        } else {
            path.transition()
                .duration(1000)
                .attrTween("d", arcTweenZoom(d));

            path2.transition()
                .duration(1000)
                .attrTween("d", arcTweenZoom(d));
        }


        $('#singleWine').hide();
        if (d.depth === 3) {

            $("#singleWine #image .content").empty();
            var imageSearch = 'search_wine.php?search=' + encodeURI(d.name);
            var image = $.post(imageSearch, function (data) {
                if (typeof data.images[0] !== "undefined") {
                    $("#singleWine #image .content")
                        .html("<img src='" + data.images[0].imageurl + "' alt='" + d.name + "' class='wineImage'/>")
                        .parent().show();
                }
            }, "json");

            $('#normalWindow').hide();
            $('#singleWine #name .content').html(d.name).parent().show();
            if (d.price) {
                $('#singleWine #price .content').html('$' + d.price).parent().show();
            }
            if (d.abv) {
                $('#singleWine #abv .content').html(d.abv).parent().show();
            }
            if (d.vintage) {
                $('#singleWine #vintage .content').html(d.vintage).parent().show();
            }
            if (d.eyes) {
                $('#singleWine #eyes .content').html(d.eyes).parent().show();
            }
            if (d.mouth) {
                $('#singleWine #mouth .content').html(d.mouth).parent().show();
            }
            if (d.nose) {
                $('#singleWine #nose .content').html(d.nose).parent().show();
            }
            if (d.overall) {
                $('#singleWine #overall .content').html(d.overall).parent().show();
            }
            if (d.producer) {
                $('#singleWine #producer .content').html(d.producer).parent().show();
            }
            if (d.region) {
                $('#singleWine #region .content').html(d.region).parent().show();
            }
            if (d.sub_region) {
                $('#singleWine #sub-region .content').html(d.sub_region).parent().show();
            }
            if (d.description) {
                $('#singleWine #description .content').html(d.description).parent().show();
            }
            $('#singleWine').show();
        }
        else if (d.depth === 2) {
            $('#singleWine').hide();
            $('#info_title').html(d.parent.name + " - " + d.name);
            $('#info_content').html("");
            $('#normalWindow').show();
            //document.getElementById("info_title").innerHTML = d.parent.name + " - " + d.name;
            //document.getElementById("info_content").innerHTML = '';
        }
        else if (d.depth === 1) {
            $('#singleWine').hide();
            $('#info_title').html(d.name);
            $('#info_content').html("");
            $('#normalWindow').show();
            //document.getElementById("info_title").innerHTML = d.name;
            //document.getElementById("info_content").innerHTML = '';
        }
        else {
            $('#singleWine').hide();
            $('#info_title').html(d.name);
            $('#info_content').html("Use the chart to browse through the wines.");
            $('#normalWindow').show();
            //document.getElementById("info_title").innerHTML = d.name;
            //document.getElementById("info_content").innerHTML = 'Use the chart to browse through the wines.';
        }
    }

    function mouseover(d) {
        // Fade all the segments.
        d3.selectAll("path")
            .style("opacity", 0.5);

        d3.select("path").style("opacity", 1);

        // Then highlight only those that are an ancestor of the current segment.
        var sequenceArray = getAncestors(d);
        d3.selectAll("path")
            .filter(function (node) {
                return (sequenceArray.indexOf(node) >= 0);
            })
            .style("opacity", 1);

        $('#sunburst_info').html(d.name);
    }

    function mouseleave(d) {
        d3.selectAll("path").style("opacity", 1);
        //$('#sunburst_info').empty();
    }

    /*
     function locationHashChanged() {
     var hash = location.hash.replace(/#/i, '');
     //var d = d3.select($('#sunburst_' + hash));
     //var d = d3.select('M1.1257428731061414e-14,-183.84776310850236A183.84776310850236,183.84776310850236 0 0,1 109.04607535919388,148.01673367817915L77.10721934826528,104.6636361129237A130,130 0 0,0 7.960204194457796e-15,-130Z');
     //var d = d3.selectAll('path#sunburst_' + hash);
     var paths = d3.select("svg").selectAll("path")[0];

     //console.log(paths);
     //console.log(hash);
     for (var i = 0; i < paths.length; i++) {
     if(paths[i]['id'] == "sunburst_"+hash) {
     console.log(paths[i]);
     }

     //console.log("MISS:", paths[i].id);
     //break;

     }
     //console.log(d);

     //node = d;
     //var path = svg.datum(root).selectAll("path");
     //arcTweenZoom(d);


     //var path = svg;
     //.data(partition.nodes)
     //.enter().append("path")
     //console.log(path);

     //path.transition()
     //    .duration(1000)
     //    .attrTween("d", arcTweenZoom(d));

     }

     window.onhashchange = locationHashChanged();
     */

});


d3.select(self.frameElement).style("height", height + "px");
// Given a node in a partition layout, return an array of all of its ancestor
// nodes, highest first, but excluding the root.
function getAncestors(node) {
    var path = [];
    var current = node;
    while (current.parent) {
        path.unshift(current);
        current = current.parent;
    }
    return path;
}
// Setup for switching data: stash the old values for transition.
function stash(d) {
    d.x0 = d.x;
    d.dx0 = d.dx;
}

// When switching data: interpolate the arcs in data space.
function arcTweenData(a, i) {
    var oi = d3.interpolate({x: a.x0, dx: a.dx0}, a);

    function tween(t) {
        var b = oi(t);
        a.x0 = b.x;
        a.dx0 = b.dx;
        return arc(b);
    }

    if (i == 0) {
        // If we are on the first arc, adjust the x domain to match the root node
        // at the current zoom level. (We only need to do this once.)
        var xd = d3.interpolate(x.domain(), [node.x, node.x + node.dx]);
        return function (t) {
            x.domain(xd(t));
            return tween(t);
        };
    } else {
        return tween;
    }
}

// When zooming: interpolate the scales.
function arcTweenZoom(d) {
    var xd = d3.interpolate(x.domain(), [d.x, d.x + d.dx]),
        yd = d3.interpolate(y.domain(), [d.y, 1]),
        yr = d3.interpolate(y.range(), [d.y ? (maxHeight / 10) : 0, radius]); //using max height to work out center
    return function (d, i) {
        return i
            ? function (t) {
            return arc(d);
        }
            : function (t) {
            x.domain(xd(t));
            y.domain(yd(t)).range(yr(t));
            return arc(d);
        };
    };
}

function computeTextRotation(d) {
    //console.group("computeTextRotation");
    //console.log("x", x(d.x + d.dx / 2));
    //console.log((x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180);
    //console.groupEnd();
    return (x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180;
}