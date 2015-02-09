module ByX
  # for each by_xyz page, collect recipes tagged with 'xyz: [a, b]'
  # into matches, keyed by `a` and `b`.
  class Generator < Jekyll::Generator
    def generate(site)
      site.pages.each do |page|
        next if ! page.name.start_with? 'by_'
        attr = page.name[3..-6]
        matches = page.data['matches'] = {}
        site.collections['recipes'].docs.each do |p|
          if p.data.include? attr
            p.data[attr].each do |v|
              if ! matches.include? v
                matches[v] = []
              end
              matches[v] << p
            end
          end
        end
      end
    end
  end
end
