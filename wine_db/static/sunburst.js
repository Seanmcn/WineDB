// Set width and height breakpoints.
var maxWidth = 500;
if (window.innerWidth < maxWidth) {
    maxWidth = window.innerWidth;
}

var maxHeight = 350;
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

var color = d3.scale.category20c();

// Mapping of step names to colors.
var colors = {
    "Red": "#DD1C1A",
    "White": "#00A6ED",
    "Rose": "#D90368",
    "N\A": "#000000"
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

    // First group should contain all items with a depth < 2.
    var group1 = data.enter().append("g").attr("class", "g-inner").filter(function (d) {
        return d.depth < 2;
    });

    // Append the item paths to group 1
    var path = group1.append("path")
        .attr("d", arc)
        .attr('id', function (d) {
            return "sunburst_" + d.name;
        })
        .style("fill", function (d) {
            if (d.color) {
                return d.color
            } else {
                return color((d.children ? d : d.parent).name)
            }
        })
        .on("click", click)
        .on("mouseover", mouseover)
        .on("mouseleave", mouseleave)
        .each(stash);

    // Playing with better rotation text
    /*
     var text = group1.append("text")
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


     .text(function (d) {
     return d.name;
     });
     */

    // Description text on first two levels
    //var text = group1.append("text")
    //    .attr("transform", function (d) {
    //        return "rotate(" + calculateRotation(d) + ")";
    //    })
    //    //.attr("transform", function (d) {
    //    //    return "rotate(" + computeTextRotation(d) + ")";
    //    //})
    //    .attr("x", function (d) {
    //        return y(d.y);
    //    })
    //    //.attr("transform", function (d) {
    //    //    return calculateX(d);
    //    //})
    //    //.attr("x", function (d) {
    //    //    return calculateX(d);
    //    //})
    //    //.attr("y", function (d) {
    //    //    return calculateY(d);
    //    //})
    //
    //    .attr("dx", "6") // margin
    //    .attr("dy", ".35em") // vertical-align
    //    .attr("fill", "white")
    //    .attr("class", "level-text-two")
    //    .text(function (d) {
    //        return d.name;
    //    });

    // Group 2 will contain all the rest of the items
    var group2 = data.enter().append("g").filter(function (d) {
        return d.depth >= 2;
    }).attr("class", "g-outer");

    // Append the item paths to group 2
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

    // Setting up the hover text SVG
    svg.append("svg:text")
        .attr("x", "0")
        //.attr("y", (maxHeight / 2) + (maxHeight / 12))
        .attr("y", 0)
        .attr("fill", "white")
        .attr("stroke", "black")
        .attr("stroke-width", "0.7")
        .attr("font-size", "18")
        .attr("font-weight", "bold")
        .attr("font-family", "sans-serif")
        .attr("text-anchor", "middle")
        .attr("id", "sunburst_info");

    // Changing the JSON data
    /*
     d3.selectAll("input").on("change", function change() {
     var value = this.value === "count"
     ? function () {
     return 1;
     }
     : function (d) {
     return d.size;
     };

     path
     .data(partition.value(value).nodes)
     .transition()
     .duration(1000)
     .attrTween("d", arcTweenData);
     });
     */

    function click(d) {
        node = d;

        console.group("Item");
        console.log(d);
        console.groupEnd();

        // Transition the path unless we are hitting level 3 and then we want to stop.
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

        // Hide things
        $('#singleWine').hide();
        $('.level-text-two').hide();

        if (d.depth === 3) {

            $('#normalWindow').hide();
            $('#singleWine #name .content').html(d.name).parent().show();
            if (d.price) {
                $('#singleWine #price .content').html('$' + d.price).parent().show();
            }
            if (d.vintage && d.vintage !== 'N/A') {
                $('#singleWine #vintage .content').html(d.vintage).parent().show();
            }
            if (d.eyes && d.eyes !== 'N/A') {
                $('#singleWine #eyes .content').html(d.eyes).parent().show();
            }
            if (d.mouth && d.mouth !== 'N/A') {
                $('#singleWine #mouth .content').html(d.mouth).parent().show();
            }
            if (d.nose && d.nose !== 'N/A') {
                $('#singleWine #nose .content').html(d.nose).parent().show();
            }
            if (d.overall && d.overall !== 'N/A') {
                $('#singleWine #overall .content').html(d.overall).parent().show();
            }
            if (d.harvested_from) {
                $('#singleWine #link .content').html("<a class='breakLink' href='" + d.harvested_from + "' target='_blank'><i class='fa fa-link'></i></a>").parent().show();
            }
            $('#sunburstViewInDB').data('name', d.name);
            $('#singleWine #db_link').show();
            $('#singleWine').show();
        }
        else if (d.depth === 2) {
            $('#singleWine').hide();
            $('#info_title').html();
            $('#info_content').html("  <ul> " +
                "<li>Hover over sunburst areas to get section name</li>" +
                "<li>Click sunburst area to facet to that section</li> " +
                "<li>Clicking a wine will replace this text with the wine information.</li>" +
                " <li>At anytime you can click on the center of the sunburst to go up a level.</li>" +
                "</ul>");
        }
        else if (d.depth === 1) {
            $('#singleWine').hide();
            $('#info_title').html();
            $('#info_content').html("  <ul> " +
                "<li>Hover over sunburst areas to get section name</li>" +
                "<li>Click sunburst area to facet to that section</li> " +
                "<li>Clicking a wine will replace this text with the wine information.</li>" +
                " <li>At anytime you can click on the center of the sunburst to go up a level.</li>" +
                "</ul>");
        }
        else {
            $('.level-text-two').show();
            $('#singleWine').hide();
            $('#info_title').html();
            $('#info_content').html("  <ul> " +
                "<li>Hover over sunburst areas to get section name</li>" +
                "<li>Click sunburst area to facet to that section</li> " +
                "<li>Clicking a wine will replace this text with the wine information.</li>" +
                " <li>At anytime you can click on the center of the sunburst to go up a level.</li>" +
                "</ul>");
            $('#normalWindow').show();
        }
    }

    function mouseover(d) {
        // Fade all the segments.
        d3.selectAll("path")
            .style("opacity", 0.5);

        // Un-fade the path we've chosen
        d3.select("path").style("opacity", 1);

        // Then un-fade those that are an ancestor of the current segment.
        var sequenceArray = getAncestors(d);
        d3.selectAll("path")
            .filter(function (node) {
                return (sequenceArray.indexOf(node) >= 0);
            })
            .style("opacity", 1);

        // Hover text
        $('#sunburst_info').html(d.name);
    }

    function mouseleave(d) {
        d3.selectAll("path").style("opacity", 1);
    }
});

d3.select(self.frameElement).style("height", height + "px");

// Given a node in a partition layout, return an array of all of its ancestor nodes, highest first, but excluding the root.
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
        // If we are on the first arc, adjust the x domain to match the root node at the current zoom level. (We only need to do this once.)
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
    return (x(d.x + d.dx / 2) - Math.PI / 2) / Math.PI * 180;
}

function calculateRotation(d) {
    console.group("Calculating Rotation for: " + d.name);
    console.log(d);
    console.groupEnd();
    //if (d.name == "") {
    //    return d.x;
    //} else {
    //    return 0;
    //}
    return computeTextRotation(d);
    //return 0;
}
function calculateX(d) {
    //return x(d.x*Math.PI);
    return y(d.y);
}
function calculateY(d) {
    return y(d.x);
    //return 0;
}