// Set width and height breakpoints.
var maxWidth = 700;
if(window.innerWidth < maxWidth ){
    maxWidth = window.innerWidth - (window.innerWidth / 8);
}

var maxHeight = 550;
if(window.innerHeight < maxHeight ){
    maxHeight = window.innerHeight - (window.innerHeight / 8);
}

var width = maxWidth,
    height = maxHeight,
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
    "Unknown": "#291720"
};

var svg = d3.select("#sunburst").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + (height / 2 + 10) + ")");

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

    //console.log(svg.data(partition.nodes(root)).selectAll(""));

//    var svgContainer = d3.select("body").append("svg")
//11                                     .attr("width",200)
//12                                     .attr("height",200);

    //var svgContainer =


    var data = svg.datum(root).selectAll("g")
        .data(partition.nodes(root));

    var group1 = data.enter().append("g").attr("class", "g-inner").filter(function(d) { return d.depth < 2; });

    //var group1Container = group1.append("g").attr("class", "g-one");

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

     var text = group1.append("text")
        .attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
        .attr("x", function(d) { return y(d.y); })
        .attr("dx", "6") // margin
        .attr("dy", ".35em") // vertical-align
        .attr("fill", "white")
        .text(function(d) { return d.name; });

    var group2 = data.enter().append("g").filter(function(d) { return d.depth >= 2; }).attr("class", "g-outer");

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


    console.log(group1);
    console.log(group2);

     //var text = g1.append("text")
     //.attr("transform", function(d) { return "rotate(" + computeTextRotation(d) + ")"; })
     //.attr("x", function(d) { return y(d.y); })
     //.attr("dx", "6") // margin
     //.attr("dy", ".35em") // vertical-align
     //.attr("fill", "white")
     //.text(function(d) { return d.name; });

    //.append("title").html(function (d) { return d.name; })

    //svg.append("svg:text")
    //    .attr("x", "0")
    //    .attr("y", "0")
    //    .attr("fill", "black")
    //    //.attr("stroke", "black")
    //    //.attr("stroke-width", "0.5")
    //    .attr("font-size", "18")
    //    .attr("font-weight", "bold")
    //    .attr("font-family", "sans-serif")
    //    .attr("text-anchor", "middle")
    //    .attr("id", "sunburst_info");
    //.text("Wines");

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
        path.transition()
            .duration(1000)
            .attrTween("d", arcTweenZoom(d));

        path2.transition()
            .duration(1000)
            .attrTween("d", arcTweenZoom(d));

        console.log(d);

        if (d.depth === 3) {
            document.getElementById("info_title").innerHTML = ""; // d.parent.parent.name + " - " + d.parent.name;
            document.getElementById("info_content").innerHTML =
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Name</div>" +
                "<div class='col-md-8'>" + d.name + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Price</div>" +
                "<div class='col-md-8'>$" + d.price + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>ABV</div>" +
                "<div class='col-md-8'>" + d.abv + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Vintage</div>" +
                "<div class='col-md-8'>" + d.vintage + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Eyes</div>" +
                "<div class='col-md-8'>" + d.eyes + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Mouth</div>" +
                "<div class='col-md-8'>" + d.mouth + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Nose</div>" +
                "<div class='col-md-8'>" + d.nose + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Overall</div>" +
                "<div class='col-md-8'>" + d.overall + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Producer</div>" +
                "<div class='col-md-8'>" + d.producer + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Region</div>" +
                "<div class='col-md-8'>" + d.region + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Sub Region</div>" +
                "<div class='col-md-8'>" + d.sub_region + "</div>" +
                "</div>" +
                "<div class='row'>" +
                "<div class='col-md-4 bold'>Description</div>" +
                "<div class='col-md-8'>" + d.description + "</div>" +
                "</div>";
        }
        else if (d.depth === 2) {
            document.getElementById("info_title").innerHTML = d.parent.name + " - " + d.name;
            document.getElementById("info_content").innerHTML = '';
        }
        else if (d.depth === 1) {
            document.getElementById("info_title").innerHTML = d.name;
            document.getElementById("info_content").innerHTML = '';
        }
        else {
            document.getElementById("info_title").innerHTML = d.name;
            document.getElementById("info_content").innerHTML = 'Use the chart to browse through the wines.';
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

        document.getElementById("sunburst_info").innerHTML = d.name;
    }

    function mouseleave(d) {
        d3.selectAll("path")
            .style("opacity", 1);
        document.getElementById("sunburst_info").innerHTML = "";
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
        yr = d3.interpolate(y.range(), [d.y ? 20 : 0, radius]);
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
    console.group("computeTextRotation");
    console.log("x", x(d.x  + d.dx /2));
    console.log((x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180);
    console.groupEnd();
    return (x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180;
}