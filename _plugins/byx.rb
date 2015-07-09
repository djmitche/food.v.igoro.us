module ByX
  # for each by_xyz page, collect recipes tagged with 'xyz: [a, b]'
  # into matches, [['a', [recipe1, recipe2]], ['b': [recipe3]]], sorted
  class Generator < Jekyll::Generator
    def generate(site)
      site.pages.each do |page|
        next if ! page.name.start_with? 'by_'
        attr = page.name[3..-6]
        matchmap = {}
        site.collections['recipes'].docs.each do |p|
          if p.data.include? attr
            p.data[attr].each do |v|
              if ! matchmap.include? v
                matchmap[v] = []
              end
              matchmap[v] << p
            end
          end
        end
        matches = page.data['matches'] = matchmap.map {|x, y| [x, y]}.sort
      end
    end
  end
end
